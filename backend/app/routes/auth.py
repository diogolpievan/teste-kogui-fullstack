from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.usuario import Usuario
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        required_fields = ['Nome', 'Login', 'Email', 'Senha']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Campo {field} é obrigatório'}), 400
        
        if Usuario.query.filter_by(Login=data['Login']).first():
            return jsonify({'error': 'Login já está em uso'}), 400
        
        if Usuario.query.filter_by(Email=data['Email']).first():
            return jsonify({'error': 'Email já está em uso'}), 400
        
        new_user = Usuario(
            Nome=data['Nome'],
            Login=data['Login'],
            Email=data['Email'],
            Senha=data['Senha']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        access_token = create_access_token(identity=new_user.IDUsuario)
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'access_token': access_token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        login = data.get('login')
        senha = data.get('senha')
        
        if not login or not senha:
            return jsonify({'error': 'Login e senha são obrigatórios'}), 400
        
        usuario = Usuario.query.filter(
            (Usuario.Login == login) | (Usuario.Email == login)
        ).first()
        
        if usuario and usuario.check_password(senha):
            access_token = create_access_token(identity=usuario.IDUsuario)
            
            return jsonify({
                'access_token': access_token,
                'user': usuario.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
            
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        usuario_id = get_jwt_identity()
        usuario = Usuario.query.get(usuario_id)
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
        return jsonify({'user': usuario.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500
