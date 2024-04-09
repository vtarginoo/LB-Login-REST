from flask import Flask, request, jsonify
from flask_login import LoginManager 
from datetime import timedelta 
from flask_jwt_extended import JWTManager,create_access_token, unset_jwt_cookies,jwt_required, get_jwt_identity
from flask_bcrypt import check_password_hash
from flask_cors import CORS

from models.user import User
from models import Session
from schemas import *

from flasgger import Swagger, LazyJSONEncoder,swag_from

import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

senha = os.getenv('SECRET_KEY')


app.json_encoder = LazyJSONEncoder

swagger_template ={
    "swagger": "2.0",
    "info": {
      "title": "Users API",
      "description": "API Documentation for Users Acess to application",
      "contact": {
        "name": "Admin",
        "email": "vtarginoo@gmail.com",
        "url": "...",
        },
      "termsOfService": "Terms of services",
      "version": "1.0",
      "basePath":"http://localhost:6050",
      "license":{
        "name":"License of API",
        "url":"API license URL"
      }
              },
    "schemes": [
        "http",
        "https"
    ],
      }

swagger_config = {
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST"),
    ],
    "specs": [
        {
            "endpoint": 'User_Access',
            "route": '/user_access.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)


# Configuração do CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Rota para lidar com solicitações OPTIONS
@app.route('/register', methods=['OPTIONS'])
def options():
    return '', 200

@swag_from("docs/register.yaml" )
@app.route("/register", methods = ["POST"])
def register():
      
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return jsonify({"message": "Username, email, and password are required."}), 400

        # Crie uma instância de sessão
        session = Session()

        # Crie uma instância de User
        user = User(username=username, email=email, password=password)

        # Adicione o usuário à sessão
        session.add(user)
        
        try:
            # Faça o commit da sessão para salvar o usuário no banco de dados
            session.commit()
            return jsonify({
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
            }), 201
        except Exception as error:
            # Em caso de erro, reverta a sessão e retorne uma mensagem de erro
            session.rollback()
            print(error)
            return jsonify({
                "message": "Por algum motivo não conseguimos fazer o cadastro do usuário.",
                "statusCode": 500
            }), 500
        finally:
            # Não se esqueça de fechar a sessão
            session.close()

@swag_from("docs/login.yaml")
@app.route("/login", methods=["POST"])
def login():
     data = request.get_json()

     # Verificar se os campos obrigatórios foram fornecidos
     if "username" not in data or "password" not in data:
         return jsonify({"msg": "Campos de usuário e senha são obrigatórios"}), 400

     # Crie uma sessão
     session = Session()

     try:
         # Verificar se o usuário existe no banco de dados
         user = session.query(User).filter_by(username=data["username"]).first()
         if not user:
             return jsonify({"msg": "Usuário não encontrado"}), 401

         # Verificar se a senha está correta
         if not check_password_hash(user.password, data["password"]):
             return jsonify({"msg": "Senha incorreta"}), 401

         # Autenticação bem-sucedida, gerar token JWT com um payload personalizado
         additional_claims = {"user_id": user.id, "username": user.username}
         access_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=30), additional_claims=additional_claims)

         return jsonify({"access_token": access_token, "additional_claims": additional_claims}), 200

     finally:
         # Não se esqueça de fechar a sessão
         session.close()


@app.route('/logout', methods=['POST'])
@jwt_required()  # Requires JWT authentication to access this route
def logout():
    """
    User Logout
    ---
    tags:
      - "Logout"
    description: User logout
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: Bearer token de autorização no formato 'Bearer <token>'
    responses:
      200:
        description: Successful logout
        schema:
          id: LogoutOutputSchema
          properties:
            message:
              type: string
              description: Mensagem indicando que o logout foi bem-sucedido.
            user_id:
              type: integer
              description: ID do usuário que fez logout.
        examples:
          application/json:
            message: Logout successful
            user_id: 1
      400:
        description: Bad request
        schema:
          id: ErrorSchema
          properties:
            message:
              type: string
              description: Mensagem de erro.
        examples:
          application/json:
            message: Erro na requisição
      401:
        description: Unauthorized
        schema:
          id: ErrorSchema
          properties:
            message:
              type: string
              description: Mensagem de erro.
        examples:
          application/json:
            message: Usuário não autorizado
    """

    
    # Obtains the identity of the current JWT token
    current_user = get_jwt_identity()

    # Clears JWT cookies from the client
    response = jsonify({"message": "Logout successful", 
                        "user_id": current_user})  # Use current_user directly
    unset_jwt_cookies(response)

    return response, 200

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=6050)





