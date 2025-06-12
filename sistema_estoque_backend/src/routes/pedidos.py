from flask import Blueprint, jsonify, request
from src.models.database import db
from src.models.pedido import PedidoML, ItemPedidoML, PagamentoML

pedidos_bp = Blueprint('pedidos', __name__)

@pedidos_bp.route('/pedidos', methods=['GET'])
def get_pedidos():
    """Listar todos os pedidos do Mercado Livre"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status', '')
    
    query = PedidoML.query
    
    # Filtro por status
    if status:
        query = query.filter(PedidoML.status == status)
    
    # Ordenar por data de criação (mais recentes primeiro)
    query = query.order_by(PedidoML.data_criacao.desc())
    
    # Paginação
    pedidos = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    return jsonify({
        'pedidos': [pedido.to_dict() for pedido in pedidos.items],
        'total': pedidos.total,
        'pages': pedidos.pages,
        'current_page': page
    })

@pedidos_bp.route('/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    """Obter um pedido específico"""
    pedido = PedidoML.query.get_or_404(pedido_id)
    return jsonify(pedido.to_dict())

@pedidos_bp.route('/pedidos', methods=['POST'])
def create_pedido():
    """Criar um novo pedido (usado para receber dados do webhook do ML)"""
    try:
        data = request.json
        
        # Verificar se o pedido já existe
        pedido_existente = PedidoML.query.get(data['id'])
        if pedido_existente:
            return jsonify({'message': 'Pedido já existe'}), 200
        
        pedido = PedidoML(
            id=data['id'],
            data_criacao=data['date_created'],
            data_fechamento=data.get('date_closed'),
            ultima_atualizacao=data['last_updated'],
            total_amount=data['total_amount'],
            paid_amount=data['paid_amount'],
            currency_id=data['currency_id'],
            status=data['status'],
            status_detalhe=data.get('status_detail'),
            ml_user_id=data.get('ml_user_id', 0),
            comprador_id=data.get('buyer', {}).get('id'),
            comprador_nickname=data.get('buyer', {}).get('nickname'),
            comprador_email=data.get('buyer', {}).get('email'),
            shipping_id=data.get('shipping', {}).get('id')
        )
        
        db.session.add(pedido)
        db.session.flush()  # Para obter o ID do pedido
        
        # Adicionar itens do pedido
        for item_data in data.get('order_items', []):
            item = ItemPedidoML(
                pedido_ml_id=pedido.id,
                ml_item_id=item_data['item']['id'],
                titulo_item=item_data['item']['title'],
                quantidade=item_data['quantity'],
                preco_unitario=item_data['unit_price']
            )
            db.session.add(item)
        
        # Adicionar pagamentos
        for payment_data in data.get('payments', []):
            pagamento = PagamentoML(
                id=payment_data['id'],
                pedido_ml_id=pedido.id,
                payer_id=payment_data.get('payer_id'),
                metodo_pagamento=payment_data.get('payment_method_id'),
                status=payment_data['status'],
                status_detalhe=payment_data.get('status_detail'),
                transaction_amount=payment_data['transaction_amount'],
                data_aprovacao=payment_data.get('date_approved'),
                data_criacao=payment_data['date_created']
            )
            db.session.add(pagamento)
        
        db.session.commit()
        return jsonify(pedido.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/pedidos/<int:pedido_id>', methods=['PUT'])
def update_pedido(pedido_id):
    """Atualizar um pedido (usado para sincronizar com ML)"""
    try:
        pedido = PedidoML.query.get_or_404(pedido_id)
        data = request.json
        
        # Atualizar campos do pedido
        pedido.data_fechamento = data.get('date_closed', pedido.data_fechamento)
        pedido.ultima_atualizacao = data.get('last_updated', pedido.ultima_atualizacao)
        pedido.total_amount = data.get('total_amount', pedido.total_amount)
        pedido.paid_amount = data.get('paid_amount', pedido.paid_amount)
        pedido.status = data.get('status', pedido.status)
        pedido.status_detalhe = data.get('status_detail', pedido.status_detalhe)
        pedido.shipping_id = data.get('shipping', {}).get('id', pedido.shipping_id)
        
        # Atualizar pagamentos se fornecidos
        if 'payments' in data:
            for payment_data in data['payments']:
                pagamento = PagamentoML.query.get(payment_data['id'])
                if pagamento:
                    pagamento.status = payment_data.get('status', pagamento.status)
                    pagamento.status_detalhe = payment_data.get('status_detail', pagamento.status_detalhe)
                    pagamento.data_aprovacao = payment_data.get('date_approved', pagamento.data_aprovacao)
        
        db.session.commit()
        return jsonify(pedido.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@pedidos_bp.route('/pedidos/status/<status>', methods=['GET'])
def get_pedidos_por_status(status):
    """Obter pedidos por status específico"""
    pedidos = PedidoML.query.filter_by(status=status).order_by(PedidoML.data_criacao.desc()).all()
    return jsonify([pedido.to_dict() for pedido in pedidos])

@pedidos_bp.route('/pedidos/estatisticas', methods=['GET'])
def get_estatisticas_pedidos():
    """Obter estatísticas dos pedidos"""
    total_pedidos = PedidoML.query.count()
    pedidos_pagos = PedidoML.query.filter_by(status='paid').count()
    pedidos_pendentes = PedidoML.query.filter_by(status='pending').count()
    
    # Valor total dos pedidos pagos
    valor_total = db.session.query(db.func.sum(PedidoML.paid_amount)).filter_by(status='paid').scalar() or 0
    
    return jsonify({
        'total_pedidos': total_pedidos,
        'pedidos_pagos': pedidos_pagos,
        'pedidos_pendentes': pedidos_pendentes,
        'valor_total_vendas': float(valor_total)
    })

