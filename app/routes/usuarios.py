from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/', methods=['GET'])
def obtener_usuarios():
    """Obtiene todos los usuarios"""
    try:
        usuarios = UsuarioService.obtener_todos_los_usuarios()
        
        return jsonify({
            'usuarios': [usuario.to_dict() for usuario in usuarios]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@usuarios_bp.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """Obtiene un usuario específico por ID"""
    try:
        usuario = UsuarioService.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'usuario': usuario.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@usuarios_bp.route('/<int:usuario_id>', methods=['PUT'])
def actualizar_usuario(usuario_id):
    """Actualiza un usuario específico"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        usuario_actualizado, error = UsuarioService.actualizar_usuario(usuario_id, data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Usuario actualizado exitosamente',
            'usuario': usuario_actualizado.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@usuarios_bp.route('/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    """Elimina un usuario (borrado lógico)"""
    try:
        resultado, error = UsuarioService.eliminar_usuario(usuario_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Usuario eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500