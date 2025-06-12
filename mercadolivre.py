from flask import Blueprint, jsonify, request, redirect
from src.services.mercadolivre_service import MercadoLivreService
from src.models.database import db
from src.models.produto import Produto

ml_bp = Blueprint('mercadolivre', __name__)
ml_service = MercadoLivreService()

@ml_bp.route('/ml/auth', methods=['GET'])
def get_auth_url():
    """Retorna a URL para autenticação OAuth do Mercado Livre"""
    try:
        auth_url = ml_service.get_auth_url()
        return jsonify({'auth_url': auth_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/callback', methods=['GET'])
def oauth_callback():
    """Callback para receber o código de autorização do Mercado Livre"""
    try:
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            return jsonify({'error': f'Erro na autorização: {error}'}), 400
        
        if not code:
            return jsonify({'error': 'Código de autorização não fornecido'}), 400
        
        # Trocar código por tokens
        token_data = ml_service.exchange_code_for_token(code)
        
        return jsonify({
            'message': 'Autorização realizada com sucesso',
            'access_token': token_data.get('access_token'),
            'user_id': token_data.get('user_id'),
            'expires_in': token_data.get('expires_in')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/webhook', methods=['POST'])
def webhook_handler():
    """Endpoint para receber notificações do Mercado Livre"""
    try:
        # Verificar se é uma requisição válida do ML
        user_id = request.args.get('user_id')
        topic = request.args.get('topic')
        
        if not user_id or not topic:
            return jsonify({'error': 'Parâmetros obrigatórios ausentes'}), 400
        
        # Processar a notificação
        notification_data = {
            'user_id': user_id,
            'topic': topic,
            'resource': request.json.get('resource') if request.json else None
        }
        
        success = ml_service.process_webhook_notification(notification_data)
        
        if success:
            return jsonify({'message': 'Notificação processada com sucesso'}), 200
        else:
            return jsonify({'error': 'Erro ao processar notificação'}), 500
            
    except Exception as e:
        print(f"Erro no webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/sync-stock/<int:produto_id>', methods=['POST'])
def sync_product_stock(produto_id):
    """Sincroniza o estoque de um produto específico com o Mercado Livre"""
    try:
        success = ml_service.sync_stock_to_ml(produto_id)
        
        if success:
            return jsonify({'message': 'Estoque sincronizado com sucesso'})
        else:
            return jsonify({'error': 'Erro ao sincronizar estoque'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/sync-all-stock', methods=['POST'])
def sync_all_stock():
    """Sincroniza o estoque de todos os produtos com ML Item ID"""
    try:
        produtos = Produto.query.filter(Produto.ml_item_id.isnot(None)).all()
        success_count = 0
        error_count = 0
        
        for produto in produtos:
            try:
                success = ml_service.sync_stock_to_ml(produto.id)
                if success:
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                print(f"Erro ao sincronizar produto {produto.id}: {str(e)}")
                error_count += 1
        
        return jsonify({
            'message': f'Sincronização concluída',
            'success_count': success_count,
            'error_count': error_count,
            'total_products': len(produtos)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/order/<order_id>', methods=['GET'])
def get_order_details(order_id):
    """Busca detalhes de um pedido específico no Mercado Livre"""
    try:
        order_details = ml_service.get_order_details(order_id)
        return jsonify(order_details)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/refresh-token', methods=['POST'])
def refresh_token():
    """Renova o token de acesso do Mercado Livre"""
    try:
        token_data = ml_service.refresh_access_token()
        return jsonify({
            'message': 'Token renovado com sucesso',
            'access_token': token_data.get('access_token'),
            'expires_in': token_data.get('expires_in')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/status', methods=['GET'])
def get_ml_status():
    """Retorna o status da integração com o Mercado Livre"""
    try:
        status = {
            'has_access_token': bool(ml_service.access_token),
            'has_refresh_token': bool(ml_service.refresh_token),
            'user_id': ml_service.user_id,
            'client_id': ml_service.client_id[:10] + '...' if ml_service.client_id else None
        }
        
        # Contar produtos com ML Item ID
        produtos_com_ml_id = Produto.query.filter(Produto.ml_item_id.isnot(None)).count()
        status['produtos_vinculados_ml'] = produtos_com_ml_id
        
        return jsonify(status)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ml_bp.route('/ml/test-connection', methods=['GET'])
def test_ml_connection():
    """Testa a conexão com a API do Mercado Livre"""
    try:
        if not ml_service.access_token:
            return jsonify({'error': 'Token de acesso não configurado'}), 400
        
        # Fazer uma requisição simples para testar
        response = ml_service.make_authenticated_request('GET', '/users/me')
        
        if response.status_code == 200:
            user_data = response.json()
            return jsonify({
                'message': 'Conexão com ML estabelecida com sucesso',
                'user_id': user_data.get('id'),
                'nickname': user_data.get('nickname'),
                'email': user_data.get('email')
            })
        else:
            return jsonify({'error': 'Falha na conexão com ML'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

