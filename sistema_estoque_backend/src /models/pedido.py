from datetime import datetime
from src.models.database import db

class PedidoML(db.Model):
    __tablename__ = 'pedidos_ml'
    
    id = db.Column(db.BigInteger, primary_key=True)
    data_criacao = db.Column(db.DateTime, nullable=False)
    data_fechamento = db.Column(db.DateTime)
    ultima_atualizacao = db.Column(db.DateTime, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency_id = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    status_detalhe = db.Column(db.String(100))
    ml_user_id = db.Column(db.BigInteger, nullable=False)
    comprador_id = db.Column(db.BigInteger)
    comprador_nickname = db.Column(db.String(100))
    comprador_email = db.Column(db.String(255))
    shipping_id = db.Column(db.BigInteger)
    
    # Relacionamentos
    itens = db.relationship('ItemPedidoML', backref='pedido', lazy=True, cascade='all, delete-orphan')
    pagamentos = db.relationship('PagamentoML', backref='pedido', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PedidoML {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_fechamento': self.data_fechamento.isoformat() if self.data_fechamento else None,
            'ultima_atualizacao': self.ultima_atualizacao.isoformat() if self.ultima_atualizacao else None,
            'total_amount': float(self.total_amount),
            'paid_amount': float(self.paid_amount),
            'currency_id': self.currency_id,
            'status': self.status,
            'status_detalhe': self.status_detalhe,
            'ml_user_id': self.ml_user_id,
            'comprador_id': self.comprador_id,
            'comprador_nickname': self.comprador_nickname,
            'comprador_email': self.comprador_email,
            'shipping_id': self.shipping_id,
            'itens': [item.to_dict() for item in self.itens],
            'pagamentos': [pag.to_dict() for pag in self.pagamentos]
        }

class ItemPedidoML(db.Model):
    __tablename__ = 'itens_pedido_ml'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_ml_id = db.Column(db.BigInteger, db.ForeignKey('pedidos_ml.id'), nullable=False)
    ml_item_id = db.Column(db.String(50), nullable=False)
    titulo_item = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    produto_interno_id = db.Column(db.Integer, db.ForeignKey('produtos.id'))
    
    # Relacionamento com produto interno (opcional)
    produto_interno = db.relationship('Produto', backref='itens_pedido_ml')
    
    def __repr__(self):
        return f'<ItemPedidoML {self.titulo_item}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_ml_id': self.pedido_ml_id,
            'ml_item_id': self.ml_item_id,
            'titulo_item': self.titulo_item,
            'quantidade': self.quantidade,
            'preco_unitario': float(self.preco_unitario),
            'produto_interno_id': self.produto_interno_id
        }

class PagamentoML(db.Model):
    __tablename__ = 'pagamentos_ml'
    
    id = db.Column(db.BigInteger, primary_key=True)
    pedido_ml_id = db.Column(db.BigInteger, db.ForeignKey('pedidos_ml.id'), nullable=False)
    payer_id = db.Column(db.BigInteger)
    metodo_pagamento = db.Column(db.String(100))
    status = db.Column(db.String(50), nullable=False)
    status_detalhe = db.Column(db.String(100))
    transaction_amount = db.Column(db.Numeric(10, 2), nullable=False)
    data_aprovacao = db.Column(db.DateTime)
    data_criacao = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<PagamentoML {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'pedido_ml_id': self.pedido_ml_id,
            'payer_id': self.payer_id,
            'metodo_pagamento': self.metodo_pagamento,
            'status': self.status,
            'status_detalhe': self.status_detalhe,
            'transaction_amount': float(self.transaction_amount),
            'data_aprovacao': self.data_aprovacao.isoformat() if self.data_aprovacao else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None
        }

