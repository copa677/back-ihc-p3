from flask import Blueprint, request, jsonify
from app.services.datos_envio_service import DatosEnvioService

datos_envio_bp = Blueprint('datos_envio', __name__)

@datos_envio_bp.route('/', methods=['POST'])
def crear_datos_envio():
    """Crea nuevos datos de envío"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = ['direccion1', 'ciudad', 'region', 'codigo_postal', 
                           'nombre_completo', 'telefono', 'usuario_id']
        
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({'error': f'El campo {campo} es requerido'}), 400
        
        datos_envio, error = DatosEnvioService.crear_datos_envio(data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Datos de envío creados exitosamente',
            'datos_envio': datos_envio.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_envio_bp.route('/', methods=['GET'])
def obtener_todos_datos_envio():
    """Obtiene todos los datos de envío"""
    try:
        datos_envio = DatosEnvioService.obtener_todos_datos_envio()
        
        return jsonify({
            'datos_envio': [de.to_dict() for de in datos_envio]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_envio_bp.route('/usuario/<int:user_telegram_id>', methods=['GET'])
def obtener_datos_envio_usuario(user_telegram_id):
    """Obtiene los datos de envío de un usuario específico"""
    try:
        datos_envio = DatosEnvioService.obtener_datos_envio_por_usuario(user_telegram_id)
        
        return jsonify({
            'datos_envio': [de.to_dict() for de in datos_envio]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_envio_bp.route('/<int:datos_envio_id>', methods=['GET'])
def obtener_datos_envio(datos_envio_id):
    """Obtiene datos de envío específicos por ID"""
    try:
        datos_envio = DatosEnvioService.obtener_datos_envio_por_id(datos_envio_id)
        if not datos_envio:
            return jsonify({'error': 'Datos de envío no encontrados'}), 404
        
        return jsonify({
            'datos_envio': datos_envio.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_envio_bp.route('/<int:datos_envio_id>', methods=['PUT'])
def actualizar_datos_envio(datos_envio_id):
    """Actualiza datos de envío"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        datos_envio_actualizado, error = DatosEnvioService.actualizar_datos_envio(datos_envio_id, data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Datos de envío actualizados exitosamente',
            'datos_envio': datos_envio_actualizado.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_envio_bp.route('/<int:datos_envio_id>', methods=['DELETE'])
def eliminar_datos_envio(datos_envio_id):
    """Elimina físicamente datos de envío"""
    try:
        resultado, error = DatosEnvioService.eliminar_datos_envio(datos_envio_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Datos de envío eliminados exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500