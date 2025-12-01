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
    
@usuarios_bp.route('/<int:delivery_id>/ubicacion', methods=['PUT'])
def actualizar_ubicacion_delivery_endpoint(delivery_id):
    """Actualiza la ubicación de un delivery y retorna su id_orden actual"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data or data.get('latitud') is None or data.get('longitud') is None:
            return jsonify({'error': 'Los campos latitud y longitud son requeridos'}), 400
        
        # Validar que sean números
        try:
            latitud = float(data['latitud'])
            longitud = float(data['longitud'])
        except ValueError:
            return jsonify({'error': 'Latitud y longitud deben ser números válidos'}), 400
        
        # Validar rangos de coordenadas (opcional)
        if not (-90 <= latitud <= 90):
            return jsonify({'error': 'Latitud debe estar entre -90 y 90'}), 400
        if not (-180 <= longitud <= 180):
            return jsonify({'error': 'Longitud debe estar entre -180 y 180'}), 400
        
        # Actualizar ubicación
        id_orden_actual, delivery, error = UsuarioService.actualizar_ubicacion_delivery(
            delivery_id=delivery_id,
            nueva_latitud=latitud,
            nueva_longitud=longitud
        )
        
        if error:
            # Si es solo un warning (delivery inactivo), igual retornamos éxito
            if "inactivo" in error.lower():
                return jsonify({
                    'warning': error,
                    'id_orden_actual': id_orden_actual,
                    'delivery': delivery.to_dict() if delivery else None
                }), 200
            return jsonify({'error': error}), 400
        
        # Si todo fue bien
        return jsonify({
            'mensaje': 'Ubicación actualizada exitosamente',
            'id_orden_actual': id_orden_actual,  # Esto es lo importante
            'delivery': delivery.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500