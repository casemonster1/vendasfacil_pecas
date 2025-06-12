import requests
import os
from datetime import datetime
from src.models.database import db
from src.models.pedido import PedidoML, ItemPedidoML, PagamentoML
from src.models.produto import Produto

class MercadoLivreService:
    def __init__(self):
        self.base_url = 'https://api.mercadolibre.com'
        self.client_id = os.getenv('ML_CLIENT_ID')
        self.client_secret = os.getenv('ML_CLIENT_SECRET')
        self.redirect_uri = os.getenv('ML_REDIRECT_URI', 'http://localhost:5001/api/ml/callback')
        self.access_token = os.getenv('ML_ACCESS_TOKEN')
        self.refresh_token = os.getenv('ML_REFRESH_TOKEN')
        self.user_id = os.getenv('ML_USER_ID')

    def get_auth_url(self):
        """Gera a URL para autenticação OAuth do Mercado Livre"""
        auth_url = f"{self.base_url}/authorization"
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'read write offline_access'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{auth_url}?{query_string}"

    def exchange_code_for_token(self, code):
        """Troca o código de autorização por tokens de acesso"""
        token_url = f"{self.base_url}/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            self.user_id = token_data.get('user_id')
            return token_data
        else:
            raise Exception(f"Erro ao obter token: {response.text}")

    def refresh_access_token(self):
        """Renova o token de acesso usando o refresh token"""
        if not self.refresh_token:
            raise Exception("Refresh token não disponível")
        
        token_url = f"{self.base_url}/oauth/token"
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            return token_data
        else:
            raise Exception(f"Erro ao renovar token: {response.text}")

    def make_authenticated_request(self, method, endpoint, data=None, params=None):
        """Faz uma requisição autenticada para a API do Mercado Livre"""
        if not self.access_token:
            raise Exception("Token de acesso não disponível")
        
        url = f"{self.base_url}{endpoint}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, params=params)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, params=params)
            else:
                raise Exception(f"Método HTTP não suportado: {method}")
            
            if response.status_code == 401:
                # Token expirado, tentar renovar
                self.refresh_access_token()
                headers['Authorization'] = f'Bearer {self.access_token}'
                
                # Repetir a requisição com o novo token
                if method.upper() == 'GET':
                    response = requests.get(url, headers=headers, params=params)
                elif method.upper() == 'POST':
                    response = requests.post(url, headers=headers, json=data, params=params)
                elif method.upper() == 'PUT':
                    response = requests.put(url, headers=headers, json=data, params=params)
            
            return response
            
        except Exception as e:
            raise Exception(f"Erro na requisição: {str(e)}")

    def get_order_details(self, order_id):
        """Busca detalhes de um pedido específico"""
        endpoint = f"/orders/{order_id}"
        response = self.make_authenticated_request('GET', endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao buscar pedido {order_id}: {response.text}")

    def update_item_stock(self, item_id, available_quantity):
        """Atualiza o estoque de um item no Mercado Livre"""
        endpoint = f"/items/{item_id}"
        data = {
            'available_quantity': available_quantity
        }
        
        response = self.make_authenticated_request('PUT', endpoint, data=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Erro ao atualizar estoque do item {item_id}: {response.text}")

    def process_webhook_notification(self, notification_data):
        """Processa uma notificação de webhook do Mercado Livre"""
        try:
            resource = notification_data.get('resource')
            topic = notification_data.get('topic')
            
            if topic == 'orders_v2':
                # Extrair o ID do pedido da URL do resource
                order_id = resource.split('/')[-1]
                
                # Buscar detalhes completos do pedido
                order_details = self.get_order_details(order_id)
                
                # Salvar ou atualizar o pedido no banco de dados
                self.save_order_to_database(order_details)
                
                # Se o pedido foi pago, atualizar o estoque
                if order_details.get('status') == 'paid':
                    self.update_stock_after_sale(order_details)
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Erro ao processar webhook: {str(e)}")
            return False

    def save_order_to_database(self, order_data):
        """Salva ou atualiza um pedido no banco de dados"""
        try:
            order_id = order_data['id']
            
            # Verificar se o pedido já existe
            existing_order = PedidoML.query.get(order_id)
            
            if existing_order:
                # Atualizar pedido existente
                existing_order.data_fechamento = self.parse_date(order_data.get('date_closed'))
                existing_order.ultima_atualizacao = self.parse_date(order_data['last_updated'])
                existing_order.total_amount = order_data['total_amount']
                existing_order.paid_amount = order_data['paid_amount']
                existing_order.status = order_data['status']
                existing_order.status_detalhe = order_data.get('status_detail')
                existing_order.shipping_id = order_data.get('shipping', {}).get('id')
            else:
                # Criar novo pedido
                new_order = PedidoML(
                    id=order_id,
                    data_criacao=self.parse_date(order_data['date_created']),
                    data_fechamento=self.parse_date(order_data.get('date_closed')),
                    ultima_atualizacao=self.parse_date(order_data['last_updated']),
                    total_amount=order_data['total_amount'],
                    paid_amount=order_data['paid_amount'],
                    currency_id=order_data['currency_id'],
                    status=order_data['status'],
                    status_detalhe=order_data.get('status_detail'),
                    ml_user_id=order_data.get('seller', {}).get('id', 0),
                    comprador_id=order_data.get('buyer', {}).get('id'),
                    comprador_nickname=order_data.get('buyer', {}).get('nickname'),
                    comprador_email=order_data.get('buyer', {}).get('email'),
                    shipping_id=order_data.get('shipping', {}).get('id')
                )
                db.session.add(new_order)
                db.session.flush()
                
                # Adicionar itens do pedido
                for item_data in order_data.get('order_items', []):
                    item = ItemPedidoML(
                        pedido_ml_id=order_id,
                        ml_item_id=item_data['item']['id'],
                        titulo_item=item_data['item']['title'],
                        quantidade=item_data['quantity'],
                        preco_unitario=item_data['unit_price']
                    )
                    
                    # Tentar mapear com produto interno
                    produto_interno = Produto.query.filter_by(ml_item_id=item_data['item']['id']).first()
                    if produto_interno:
                        item.produto_interno_id = produto_interno.id
                    
                    db.session.add(item)
                
                # Adicionar pagamentos
                for payment_data in order_data.get('payments', []):
                    pagamento = PagamentoML(
                        id=payment_data['id'],
                        pedido_ml_id=order_id,
                        payer_id=payment_data.get('payer_id'),
                        metodo_pagamento=payment_data.get('payment_method_id'),
                        status=payment_data['status'],
                        status_detalhe=payment_data.get('status_detail'),
                        transaction_amount=payment_data['transaction_amount'],
                        data_aprovacao=self.parse_date(payment_data.get('date_approved')),
                        data_criacao=self.parse_date(payment_data['date_created'])
                    )
                    db.session.add(pagamento)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao salvar pedido no banco: {str(e)}")
            return False

    def update_stock_after_sale(self, order_data):
        """Atualiza o estoque interno após uma venda"""
        try:
            for item_data in order_data.get('order_items', []):
                produto = Produto.query.filter_by(ml_item_id=item_data['item']['id']).first()
                
                if produto:
                    # Reduzir a quantidade do estoque
                    quantidade_vendida = item_data['quantity']
                    produto.quantidade_estoque = max(0, produto.quantidade_estoque - quantidade_vendida)
                    
                    # Atualizar timestamp de sincronização
                    produto.ml_last_sync = datetime.utcnow()
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao atualizar estoque após venda: {str(e)}")
            return False

    def sync_stock_to_ml(self, produto_id):
        """Sincroniza o estoque de um produto com o Mercado Livre"""
        try:
            produto = Produto.query.get(produto_id)
            
            if not produto or not produto.ml_item_id:
                return False
            
            # Atualizar estoque no ML
            response_data = self.update_item_stock(produto.ml_item_id, produto.quantidade_estoque)
            
            # Atualizar timestamp de sincronização
            produto.ml_last_sync = datetime.utcnow()
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"Erro ao sincronizar estoque: {str(e)}")
            return False

    def parse_date(self, date_string):
        """Converte string de data do ML para datetime"""
        if not date_string:
            return None
        
        try:
            # Formato: 2023-12-01T10:30:00.000-03:00
            # Remover timezone para simplificar
            if '+' in date_string:
                date_string = date_string.split('+')[0]
            elif date_string.endswith('Z'):
                date_string = date_string[:-1]
            elif '-' in date_string[-6:]:
                date_string = date_string[:-6]
            
            # Remover milissegundos se presentes
            if '.' in date_string:
                date_string = date_string.split('.')[0]
            
            return datetime.fromisoformat(date_string)
            
        except Exception as e:
            print(f"Erro ao converter data {date_string}: {str(e)}")
            return None

