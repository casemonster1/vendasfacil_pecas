# sistema_estoque_backend/src/main.py

import os
import sys

# DON\'T CHANGE THE LINES BELOW
# This is to allow the app to be run from the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(project_root)
# DON\'T CHANGE THE LINES ABOVE

from flask import Flask, jsonify
from flask_cors import CORS
from src.models.database import db

# Importar blueprints
from src.routes.produtos import produtos_bp
from src.routes.pedidos import pedidos_bp
from src.routes.usuarios import usuarios_bp
from src.routes.mercadolivre import mercadolivre_bp
from src.routes.auth import auth_bp

app = Flask(__name__)
CORS(app) # Habilitar CORS para todas as rotas

# Configuração do banco de dados
# Use a variável de ambiente DATABASE_URL fornecida pelo Render
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///estoque.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(produtos_bp, url_prefix="/api/produtos")
app.register_blueprint(pedidos_bp, url_prefix="/api/pedidos")
app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
app.register_blueprint(mercadolivre_bp, url_prefix="/api/ml")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Rota de teste
@app.route("/")
def home():
    return jsonify({"message": "Bem-vindo ao Sistema de Estoque de Peças de Carro!"})

# Criar tabelas do banco de dados se não existirem
with app.app_context():
    db.create_all()

if __name__ == \'__main__\':
    # Use a porta fornecida pelo Render (PORT) ou 5001 para desenvolvimento local
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)

