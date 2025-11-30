from flask import Blueprint, request, jsonify
from app.services.user_telegram import UserTelegramService

user_telegram_bp = Blueprint('user_telegram', __name__)

@user_telegram_bp.route('/', methods=['POST'])
def create_or_get_user_telegram():
    """
    Endpoint único para insertar o verificar usuario de Telegram
    Si el chat_id no existe, lo crea. Si existe, retorna el existente.
    """
    try:
        data = request.get_json()
        
        if not data or 'chat_id' not in data:
            return jsonify({
                'error': 'El campo chat_id es requerido'
            }), 400

        chat_id = str(data['chat_id']).strip()
        
        if not chat_id:
            return jsonify({
                'error': 'chat_id no puede estar vacío'
            }), 400

        # Usar el servicio para crear o obtener el usuario
        user, created = UserTelegramService.create_user_telegram(chat_id)
        
        response_data = {
            'user': user.to_dict(),
            'created': created,
            'message': 'Usuario creado exitosamente' if created else 'El usuario ya existe'
        }
        
        status_code = 201 if created else 200
        
        return jsonify(response_data), status_code

    except Exception as e:
        return jsonify({
            'error': f'Error al procesar la solicitud: {str(e)}'
        }), 500

@user_telegram_bp.route('/', methods=['GET'])
def get_all_users_telegram():
    """Obtiene todos los usuarios de Telegram"""
    try:
        users = UserTelegramService.get_all_users()
        
        users_data = [user.to_dict() for user in users]
        
        return jsonify({
            'users': users_data,
            'count': len(users_data)
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Error al obtener los usuarios: {str(e)}'
        }), 500

@user_telegram_bp.route('/<int:user_id>', methods=['GET'])
def get_user_telegram_by_id(user_id):
    """Obtiene un usuario de Telegram por ID"""
    try:
        user = UserTelegramService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'error': 'Usuario no encontrado'
            }), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Error al obtener el usuario: {str(e)}'
        }), 500

@user_telegram_bp.route('/chat/<chat_id>', methods=['GET'])
def get_user_telegram_by_chat_id(chat_id):
    """Obtiene un usuario de Telegram por chat_id"""
    try:
        user = UserTelegramService.get_user_by_chat_id(chat_id)
        
        if not user:
            return jsonify({
                'error': 'Usuario no encontrado'
            }), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Error al obtener el usuario: {str(e)}'
        }), 500