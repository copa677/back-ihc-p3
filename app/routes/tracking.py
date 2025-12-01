from flask import Blueprint, request, jsonify
from app.services.tracking_service import TrackingService
from app.services.usuario_service import UsuarioService

tracking_bp = Blueprint('tracking', __name__)

# ==================== CRUD BÁSICO ====================

@tracking_bp.route('/', methods=['POST'])
def crear_tracking():
    """Crea un nuevo registro de tracking"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = ['orden_cod', 'user_delivery_id', 'estado']
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({'error': f'El campo {campo} es requerido'}), 400
        
        # Validar que el estado sea válido
        estados_validos = ['asignada', 'recogiendo', 'en_camino', 'entregada', 'cancelada']
        if data['estado'] not in estados_validos:
            return jsonify({
                'error': f'Estado no válido. Debe ser uno de: {", ".join(estados_validos)}'
            }), 400
        
        # Crear tracking
        tracking, error = TrackingService.crear_tracking(
            orden_cod=data['orden_cod'],
            user_delivery_id=data['user_delivery_id'],
            estado=data['estado'],
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            comentario=data.get('comentario')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Tracking creado exitosamente',
            'tracking': tracking.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500


@tracking_bp.route('/<int:tracking_id>', methods=['GET'])
def obtener_tracking(tracking_id):
    """Obtiene un tracking específico por ID"""
    try:
        tracking = TrackingService.obtener_tracking_por_id(tracking_id)
        
        if not tracking:
            return jsonify({'error': 'Tracking no encontrado'}), 404
        
        return jsonify({
            'tracking': tracking.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500


@tracking_bp.route('/<int:tracking_id>', methods=['PUT'])
def actualizar_tracking(tracking_id):
    """Actualiza un tracking existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        # Validar que el estado sea válido si se está actualizando
        if 'estado' in data:
            estados_validos = ['asignada', 'recogiendo', 'en_camino', 'entregada', 'cancelada']
            if data['estado'] not in estados_validos:
                return jsonify({
                    'error': f'Estado no válido. Debe ser uno de: {", ".join(estados_validos)}'
                }), 400
        
        # Actualizar tracking
        tracking_actualizado, error = TrackingService.actualizar_tracking(tracking_id, data)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Tracking actualizado exitosamente',
            'tracking': tracking_actualizado.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500


@tracking_bp.route('/<int:tracking_id>', methods=['DELETE'])
def eliminar_tracking(tracking_id):
    """Elimina un registro de tracking"""
    try:
        resultado, error = TrackingService.eliminar_tracking(tracking_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Tracking eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

# ==================== HISTORIAL POR DELIVERY ====================

@tracking_bp.route('/delivery/<int:delivery_id>/historial', methods=['GET'])
def obtener_historial_delivery(delivery_id):
    """Obtiene el historial de tracking de un delivery específico"""
    try:
        # Verificar que el delivery existe
        delivery = UsuarioService.obtener_usuario_por_id(delivery_id)
        if not delivery:
            return jsonify({'error': 'Delivery no encontrado'}), 404
        
        # Obtener parámetros de consulta
        limit = request.args.get('limit', type=int)
        
        # Obtener historial
        historial = TrackingService.obtener_historial_por_delivery(delivery_id, limit=limit)
        
        return jsonify({
            'delivery_id': delivery_id,
            'delivery_username': delivery.username,
            'limit': limit,
            'historial': [tracking.to_dict() for tracking in historial],
            'total_registros': len(historial)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

# ==================== HISTORIAL POR ORDEN (EXTRA ÚTIL) ====================

@tracking_bp.route('/orden/<int:orden_cod>/historial', methods=['GET'])
def obtener_historial_orden(orden_cod):
    """Obtiene el historial de tracking de una orden específica"""
    try:
        historial = TrackingService.obtener_trackings_por_orden(orden_cod)
        
        return jsonify({
            'orden_cod': orden_cod,
            'historial': [tracking.to_dict() for tracking in historial],
            'total_registros': len(historial)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500