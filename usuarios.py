from flask import Blueprint, jsonify, request
from src.models.database import db
from src.models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    """Listar todos os usuários"""
    usuarios = Usuario.query.filter_by(ativo=True).all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@usuarios_bp.route('/usuarios', methods=['POST'])
def create_usuario():
    """Criar um novo usuário"""
    try:
        data = request.json
        
        # Validações básicas
        if not data.get('nome') or not data.get('email') or not data.get('senha'):
            return jsonify({'error': 'Nome, email e senha são obrigatórios'}), 400
        
        # Verificar se email já existe
        if Usuario.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já existe'}), 400
        
        usuario = Usuario(
            nome=data['nome'],
            email=data['email'],
            role=data.get('role', 'estoque')
        )
        usuario.set_password(data['senha'])
        
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify(usuario.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):
    """Obter um usuário específico"""
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify(usuario.to_dict())

@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def update_usuario(usuario_id):
    """Atualizar um usuário"""
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        data = request.json
        
        usuario.nome = data.get('nome', usuario.nome)
        usuario.email = data.get('email', usuario.email)
        usuario.role = data.get('role', usuario.role)
        usuario.ativo = data.get('ativo', usuario.ativo)
        
        # Atualizar senha se fornecida
        if data.get('senha'):
            usuario.set_password(data['senha'])
        
        db.session.commit()
        return jsonify(usuario.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def delete_usuario(usuario_id):
    """Desativar um usuário (soft delete)"""
    try:
        usuario = Usuario.query.get_or_404(usuario_id)
        usuario.ativo = False
        db.session.commit()
        return '', 204
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@usuarios_bp.route('/auth/login', methods=['POST'])
def login():
    """Autenticar um usuário"""
    try:
        data = request.json
        
        if not data.get('email') or not data.get('senha'):
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        usuario = Usuario.query.filter_by(email=data['email'], ativo=True).first()
        
        if not usuario or not usuario.check_password(data['senha']):
            return jsonify({'error': 'Credenciais inválidas'}), 401
        
        # Em uma implementação real, aqui seria gerado um JWT token
        return jsonify({
            'message': 'Login realizado com sucesso',
            'usuario': usuario.to_dict()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

