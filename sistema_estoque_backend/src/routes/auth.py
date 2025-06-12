# sistema_estoque_backend/src/routes/auth.py

from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.database import db
from src.models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")
    role = data.get("role", "estoque") # Default role is 'estoque'

    if not nome or not email or not senha:
        return jsonify({"message": "Nome, email e senha são obrigatórios"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"message": "Email já registrado"}), 409

    hashed_password = generate_password_hash(senha, method="pbkdf2:sha256")
    new_user = Usuario(nome=nome, email=email, senha=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"message": "Email e senha são obrigatórios"}), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.senha, senha):
        return jsonify({"message": "Credenciais inválidas"}), 401

    # Aqui você pode gerar um token JWT ou gerenciar a sessão de outra forma
    # Por simplicidade, vamos retornar apenas uma mensagem de sucesso e o role do usuário
    return jsonify({"message": "Login bem-sucedido!", "user_id": user.id, "user_role": user.role}), 200

