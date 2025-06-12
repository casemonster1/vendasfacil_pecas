from flask import Blueprint, jsonify, request
from src.models.database import db
from src.models.produto import Produto, ImagemProduto, VeiculoCompativel

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos', methods=['GET'])
def get_produtos():
    """Listar todos os produtos"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')
    
    query = Produto.query
    
    # Filtros
    if search:
        query = query.filter(
            (Produto.nome.contains(search)) |
            (Produto.referencia_sku.contains(search)) |
            (Produto.descricao.contains(search))
        )
    
    if categoria:
        query = query.filter(Produto.categoria == categoria)
    
    # Paginação
    produtos = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'produtos': [produto.to_dict() for produto in produtos.items],
        'total': produtos.total,
        'pages': produtos.pages,
        'current_page': page
    })

@produtos_bp.route('/produtos', methods=['POST'])
def create_produto():
    """Criar um novo produto"""
    try:
        data = request.json
        
        # Validações básicas
        if not data.get('nome') or not data.get('referencia_sku'):
            return jsonify({'error': 'Nome e referência SKU são obrigatórios'}), 400
        
        # Verificar se SKU já existe
        if Produto.query.filter_by(referencia_sku=data['referencia_sku']).first():
            return jsonify({'error': 'SKU já existe'}), 400
        
        produto = Produto(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            referencia_sku=data['referencia_sku'],
            preco_venda=data.get('preco_venda', 0),
            quantidade_estoque=data.get('quantidade_estoque', 0),
            localizacao_galpao=data.get('localizacao_galpao'),
            categoria=data.get('categoria'),
            subcategoria=data.get('subcategoria'),
            marca_peca=data.get('marca_peca'),
            condicao=data.get('condicao', 'Novo'),
            ml_item_id=data.get('ml_item_id')
        )
        
        db.session.add(produto)
        db.session.flush()  # Para obter o ID do produto
        
        # Adicionar imagens se fornecidas
        if data.get('imagens'):
            for i, imagem_path in enumerate(data['imagens']):
                imagem = ImagemProduto(
                    produto_id=produto.id,
                    caminho_imagem=imagem_path,
                    ordem=i + 1
                )
                db.session.add(imagem)
        
        # Adicionar veículos compatíveis se fornecidos
        if data.get('veiculos_compativeis'):
            for veiculo_data in data['veiculos_compativeis']:
                veiculo = VeiculoCompativel(
                    produto_id=produto.id,
                    marca_veiculo=veiculo_data['marca_veiculo'],
                    modelo_veiculo=veiculo_data['modelo_veiculo'],
                    ano_inicial=veiculo_data.get('ano_inicial'),
                    ano_final=veiculo_data.get('ano_final')
                )
                db.session.add(veiculo)
        
        db.session.commit()
        return jsonify(produto.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):
    """Obter um produto específico"""
    produto = Produto.query.get_or_404(produto_id)
    return jsonify(produto.to_dict())

@produtos_bp.route('/produtos/<int:produto_id>', methods=['PUT'])
def update_produto(produto_id):
    """Atualizar um produto"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        data = request.json
        
        # Atualizar campos básicos
        produto.nome = data.get('nome', produto.nome)
        produto.descricao = data.get('descricao', produto.descricao)
        produto.preco_venda = data.get('preco_venda', produto.preco_venda)
        produto.quantidade_estoque = data.get('quantidade_estoque', produto.quantidade_estoque)
        produto.localizacao_galpao = data.get('localizacao_galpao', produto.localizacao_galpao)
        produto.categoria = data.get('categoria', produto.categoria)
        produto.subcategoria = data.get('subcategoria', produto.subcategoria)
        produto.marca_peca = data.get('marca_peca', produto.marca_peca)
        produto.condicao = data.get('condicao', produto.condicao)
        produto.ml_item_id = data.get('ml_item_id', produto.ml_item_id)
        
        # Atualizar imagens se fornecidas
        if 'imagens' in data:
            # Remover imagens existentes
            ImagemProduto.query.filter_by(produto_id=produto.id).delete()
            
            # Adicionar novas imagens
            for i, imagem_path in enumerate(data['imagens']):
                imagem = ImagemProduto(
                    produto_id=produto.id,
                    caminho_imagem=imagem_path,
                    ordem=i + 1
                )
                db.session.add(imagem)
        
        # Atualizar veículos compatíveis se fornecidos
        if 'veiculos_compativeis' in data:
            # Remover veículos existentes
            VeiculoCompativel.query.filter_by(produto_id=produto.id).delete()
            
            # Adicionar novos veículos
            for veiculo_data in data['veiculos_compativeis']:
                veiculo = VeiculoCompativel(
                    produto_id=produto.id,
                    marca_veiculo=veiculo_data['marca_veiculo'],
                    modelo_veiculo=veiculo_data['modelo_veiculo'],
                    ano_inicial=veiculo_data.get('ano_inicial'),
                    ano_final=veiculo_data.get('ano_final')
                )
                db.session.add(veiculo)
        
        db.session.commit()
        return jsonify(produto.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/<int:produto_id>', methods=['DELETE'])
def delete_produto(produto_id):
    """Deletar um produto"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        db.session.delete(produto)
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/<int:produto_id>/estoque', methods=['PUT'])
def update_estoque(produto_id):
    """Atualizar apenas o estoque de um produto"""
    try:
        produto = Produto.query.get_or_404(produto_id)
        data = request.json
        
        if 'quantidade_estoque' not in data:
            return jsonify({'error': 'quantidade_estoque é obrigatória'}), 400
        
        produto.quantidade_estoque = data['quantidade_estoque']
        db.session.commit()
        
        return jsonify({
            'id': produto.id,
            'nome': produto.nome,
            'quantidade_estoque': produto.quantidade_estoque
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@produtos_bp.route('/produtos/categorias', methods=['GET'])
def get_categorias():
    """Obter lista de categorias únicas"""
    categorias = db.session.query(Produto.categoria).distinct().filter(Produto.categoria.isnot(None)).all()
    return jsonify([cat[0] for cat in categorias if cat[0]])

@produtos_bp.route('/produtos/estoque-baixo', methods=['GET'])
def get_produtos_estoque_baixo():
    """Obter produtos com estoque baixo (menos de 5 unidades)"""
    limite = request.args.get('limite', 5, type=int)
    produtos = Produto.query.filter(Produto.quantidade_estoque <= limite).all()
    return jsonify([produto.to_dict() for produto in produtos])

