from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.usuario_service import UsuarioService
from app.utils.security import crear_token_usuario, extraer_datos_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['POST'])
def registro():
    """Registra un nuevo usuario"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'error': 'Se requieren username y password'
            }), 400
        
        # Crear usuario
        usuario, error = UsuarioService.crear_usuario(
            username=data.get('username'),
            password=data.get('password'),
            tipo_usuario=data.get('tipo_usuario', 'usuario')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        # Crear token
        token = crear_token_usuario(usuario)
        
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'token': token,
            'usuario': usuario.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicia sesión y devuelve token JWT"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'error': 'Se requieren username y password'
            }), 400
        
        # Autenticar usuario
        usuario, error = UsuarioService.autenticar_usuario(
            username=data.get('username'),
            password=data.get('password')
        )
        
        if error:
            return jsonify({'error': error}), 401
        
        # Crear token
        token = crear_token_usuario(usuario)
        
        return jsonify({
            'mensaje': 'Login exitoso',
            'token': token,
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def obtener_usuario_actual():
    """Obtiene la información del usuario actual basado en el token"""
    try:
        identity = get_jwt_identity()
        datos_usuario = extraer_datos_token(identity)
        
        usuario = UsuarioService.obtener_usuario_por_id(datos_usuario['id'])
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500