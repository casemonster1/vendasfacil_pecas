from datetime import datetime
from src.models.database import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    referencia_sku = db.Column(db.String(100), unique=True, nullable=False)
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False, default=0)
    localizacao_galpao = db.Column(db.String(100))
    categoria = db.Column(db.String(100))
    subcategoria = db.Column(db.String(100))
    marca_peca = db.Column(db.String(100))
    condicao = db.Column(db.String(50), nullable=False)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ml_item_id = db.Column(db.String(50), unique=True)
    ml_last_sync = db.Column(db.DateTime)
    
    # Relacionamentos
    imagens = db.relationship('ImagemProduto', backref='produto', lazy=True, cascade='all, delete-orphan')
    veiculos_compativeis = db.relationship('VeiculoCompativel', backref='produto', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Produto {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'referencia_sku': self.referencia_sku,
            'preco_venda': float(self.preco_venda),
            'quantidade_estoque': self.quantidade_estoque,
            'localizacao_galpao': self.localizacao_galpao,
            'categoria': self.categoria,
            'subcategoria': self.subcategoria,
            'marca_peca': self.marca_peca,
            'condicao': self.condicao,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'data_atualizacao': self.data_atualizacao.isoformat() if self.data_atualizacao else None,
            'ml_item_id': self.ml_item_id,
            'ml_last_sync': self.ml_last_sync.isoformat() if self.ml_last_sync else None,
            'imagens': [img.to_dict() for img in self.imagens],
            'veiculos_compativeis': [vc.to_dict() for vc in self.veiculos_compativeis]
        }

class ImagemProduto(db.Model):
    __tablename__ = 'imagens_produto'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    caminho_imagem = db.Column(db.String(255), nullable=False)
    ordem = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<ImagemProduto {self.caminho_imagem}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'caminho_imagem': self.caminho_imagem,
            'ordem': self.ordem
        }

class VeiculoCompativel(db.Model):
    __tablename__ = 'veiculos_compativeis'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    marca_veiculo = db.Column(db.String(100), nullable=False)
    modelo_veiculo = db.Column(db.String(100), nullable=False)
    ano_inicial = db.Column(db.Integer)
    ano_final = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<VeiculoCompativel {self.marca_veiculo} {self.modelo_veiculo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'produto_id': self.produto_id,
            'marca_veiculo': self.marca_veiculo,
            'modelo_veiculo': self.modelo_veiculo,
            'ano_inicial': self.ano_inicial,
            'ano_final': self.ano_final
        }

