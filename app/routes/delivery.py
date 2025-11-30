from flask import Blueprint, request, jsonify
from app.services.notificacion_service import NotificacionService
from app.services.tracking_service import TrackingService

delivery_bp = Blueprint('delivery', __name__)

@delivery_bp.route('/notificaciones/<int:user_delivery_id>', methods=['GET'])
def obtener_notificaciones_pendientes(user_delivery_id):
    """Endpoint para polling de notificaciones (cada 5 segundos)"""
    try:
        notificaciones = NotificacionService.obtener_notificaciones_pendientes(user_delivery_id)
        
        return jsonify({
            'notificaciones': [n.to_dict() for n in notificaciones],
            'count': len(notificaciones)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@delivery_bp.route('/notificacion/<int:notificacion_id>/responder', methods=['POST'])
def responder_notificacion(notificacion_id):
    """Delivery acepta o rechaza la orden"""
    try:
        data = request.get_json()
        
        if not data or not data.get('respuesta'):
            return jsonify({'error': 'El campo respuesta es requerido'}), 400
        
        respuesta = data.get('respuesta')
        
        notificacion, mensaje = NotificacionService.responder_notificacion(notificacion_id, respuesta)
        if not notificacion:
            return jsonify({'error': mensaje}), 400
        
        return jsonify({
            'mensaje': mensaje,
            'notificacion': notificacion.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@delivery_bp.route('/tracking/<int:orden_cod>/actualizar', methods=['POST'])
def actualizar_tracking(orden_cod):
    """Delivery actualiza su ubicación y estado"""
    try:
        data = request.get_json()
        
        tracking, error = TrackingService.actualizar_tracking(orden_cod, data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Tracking actualizado exitosamente',
            'tracking': tracking.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@delivery_bp.route('/tracking/<int:orden_cod>', methods=['GET'])
def obtener_tracking(orden_cod):
    """Obtiene el tracking de una orden específica"""
    try:
        tracking = TrackingService.obtener_tracking_por_orden(orden_cod)
        if not tracking:
            return jsonify({'error': 'No hay tracking para esta orden'}), 404
        
        return jsonify({
            'tracking': tracking.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500