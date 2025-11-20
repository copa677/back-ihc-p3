from flask import Blueprint, request, jsonify
from app.services.datos_pago_service import DatosPagoService

datos_pago_bp = Blueprint('datos_pago', __name__)

@datos_pago_bp.route('/', methods=['POST'])
def crear_datos_pago():
    """Crea nuevos datos de pago"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = ['numero_tarjeta', 'fecha_expiracion_tarjeta', 
                           'nombre_propietario', 'codigo_seguridad', 'pais', 
                           'codigo_postal', 'usuario_id']
        
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({'error': f'El campo {campo} es requerido'}), 400
        
        datos_pago, error = DatosPagoService.crear_datos_pago(data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Datos de pago creados exitosamente',
            'datos_pago': datos_pago.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_pago_bp.route('/', methods=['GET'])
def obtener_todos_datos_pago():
    """Obtiene todos los datos de pago"""
    try:
        datos_pago = DatosPagoService.obtener_todos_datos_pago()
        
        return jsonify({
            'datos_pago': [dp.to_dict() for dp in datos_pago]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_pago_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_datos_pago_usuario(usuario_id):
    """Obtiene los datos de pago de un usuario específico"""
    try:
        datos_pago = DatosPagoService.obtener_datos_pago_por_usuario(usuario_id)
        
        return jsonify({
            'datos_pago': [dp.to_dict() for dp in datos_pago]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_pago_bp.route('/<int:datos_pago_id>', methods=['GET'])
def obtener_datos_pago(datos_pago_id):
    """Obtiene datos de pago específicos por ID"""
    try:
        datos_pago = DatosPagoService.obtener_datos_pago_por_id(datos_pago_id)
        if not datos_pago:
            return jsonify({'error': 'Datos de pago no encontrados'}), 404
        
        return jsonify({
            'datos_pago': datos_pago.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_pago_bp.route('/<int:datos_pago_id>', methods=['PUT'])
def actualizar_datos_pago(datos_pago_id):
    """Actualiza datos de pago"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        datos_pago_actualizado, error = DatosPagoService.actualizar_datos_pago(datos_pago_id, data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Datos de pago actualizados exitosamente',
            'datos_pago': datos_pago_actualizado.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@datos_pago_bp.route('/<int:datos_pago_id>', methods=['DELETE'])
def eliminar_datos_pago(datos_pago_id):
    """Elimina físicamente datos de pago"""
    try:
        resultado, error = DatosPagoService.eliminar_datos_pago(datos_pago_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Datos de pago eliminados exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500