from flask import Blueprint, request, jsonify
from app.services.orden_service import OrdenService
from app.services.factura_service import FacturaService

orden_bp = Blueprint('orden', __name__)

@orden_bp.route('/', methods=['POST'])
def crear_orden():
    """Crea una nueva orden"""
    try:
        data = request.get_json()
        
        if not data or not data.get('user_telegram_id'):
            return jsonify({'error': 'El campo usuario_id es requerido'}), 400
        
        orden, error = OrdenService.crear_orden(
            user_telegram_id=data['user_telegram_id'],
            estado=data.get('estado', 'pendiente')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Orden creada exitosamente',
            'orden': orden.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/', methods=['GET'])
def obtener_todas_ordenes():
    """Obtiene todas las órdenes"""
    try:
        ordenes = OrdenService.obtener_todas_ordenes()
        
        ordenes_con_detalles = []
        for orden in ordenes:
            detalles = OrdenService.obtener_detalles_orden(orden.cod)
            factura = FacturaService.obtener_facturas_por_orden(orden.cod)
            
            orden_dict = orden.to_dict()
            orden_dict['detalles'] = [detalle.to_dict() for detalle in detalles]
            orden_dict['factura'] = factura.to_dict() if factura else None
            ordenes_con_detalles.append(orden_dict)
        
        return jsonify({
            'ordenes': ordenes_con_detalles
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/usuario/<int:user_telegram_id>', methods=['GET'])
def obtener_ordenes_usuario(user_telegram_id):
    """Obtiene todas las órdenes de un usuario"""
    try:
        ordenes = OrdenService.obtener_ordenes_por_usuario(user_telegram_id)
        
        ordenes_con_detalles = []
        for orden in ordenes:
            detalles = OrdenService.obtener_detalles_orden(orden.cod)
            factura = FacturaService.obtener_facturas_por_orden(orden.cod)
            
            orden_dict = orden.to_dict()
            orden_dict['detalles'] = [detalle.to_dict() for detalle in detalles]
            orden_dict['factura'] = factura.to_dict() if factura else None
            ordenes_con_detalles.append(orden_dict)
        
        return jsonify({
            'ordenes': ordenes_con_detalles
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/estado/<string:estado>', methods=['GET'])
def obtener_ordenes_por_estado(estado):
    """Obtiene órdenes por estado"""
    try:
        ordenes = OrdenService.obtener_ordenes_por_estado(estado)
        
        ordenes_con_detalles = []
        for orden in ordenes:
            detalles = OrdenService.obtener_detalles_orden(orden.cod)
            factura = FacturaService.obtener_facturas_por_orden(orden.cod)
            
            orden_dict = orden.to_dict()
            orden_dict['detalles'] = [detalle.to_dict() for detalle in detalles]
            orden_dict['factura'] = factura.to_dict() if factura else None
            ordenes_con_detalles.append(orden_dict)
        
        return jsonify({
            'ordenes': ordenes_con_detalles,
            'estado': estado
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/<int:orden_cod>', methods=['GET'])
def obtener_orden(orden_cod):
    """Obtiene una orden específica por código"""
    try:
        orden = OrdenService.obtener_orden_por_cod(orden_cod)
        if not orden:
            return jsonify({'error': 'Orden no encontrada'}), 404
        
        detalles = OrdenService.obtener_detalles_orden(orden_cod)
        factura = FacturaService.obtener_facturas_por_orden(orden_cod)
        
        return jsonify({
            'orden': orden.to_dict(),
            'detalles': [detalle.to_dict() for detalle in detalles],
            'factura': factura.to_dict() if factura else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/<int:orden_cod>/agregar-detalle', methods=['POST'])
def agregar_detalle_orden(orden_cod):
    """Agrega un detalle a la orden"""
    try:
        data = request.get_json()
        
        if not data or not data.get('producto_id') or not data.get('cantidad') or not data.get('precio_unitario'):
            return jsonify({'error': 'Los campos producto_id, cantidad y precio_unitario son requeridos'}), 400
        
        detalle, error = OrdenService.agregar_detalle_orden(
            orden_cod=orden_cod,
            producto_id=data['producto_id'],
            cantidad=data['cantidad'],
            precio_unitario=data['precio_unitario']
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Detalle agregado a la orden exitosamente',
            'detalle': detalle.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/<int:orden_cod>/estado', methods=['PUT'])
def actualizar_estado_orden(orden_cod):
    """Actualiza el estado de una orden"""
    try:
        data = request.get_json()
        
        if not data or not data.get('estado'):
            return jsonify({'error': 'El campo estado es requerido'}), 400
        
        orden, error = OrdenService.actualizar_estado_orden(orden_cod, data['estado'])
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Estado de orden actualizado exitosamente',
            'orden': orden.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/detalle/<int:detalle_id>', methods=['PUT'])
def actualizar_detalle_orden(detalle_id):
    """Actualiza la cantidad de un detalle"""
    try:
        data = request.get_json()
        
        if not data or data.get('cantidad') is None:
            return jsonify({'error': 'El campo cantidad es requerido'}), 400
        
        detalle, error = OrdenService.actualizar_detalle_orden(detalle_id, data['cantidad'])
        if error:
            return jsonify({'error': error}), 400
        
        if detalle:  # Si se actualizó la cantidad
            return jsonify({
                'mensaje': 'Detalle actualizado exitosamente',
                'detalle': detalle.to_dict()
            }), 200
        else:  # Si se eliminó el detalle (cantidad = 0)
            return jsonify({
                'mensaje': 'Detalle eliminado de la orden'
            }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/detalle/<int:detalle_id>', methods=['DELETE'])
def eliminar_detalle_orden(detalle_id):
    """Elimina un detalle de la orden"""
    try:
        resultado, error = OrdenService.eliminar_detalle_orden(detalle_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Detalle eliminado de la orden exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/<int:orden_cod>/factura', methods=['POST'])
def crear_factura_desde_orden(orden_cod):
    """Crea una factura a partir de una orden"""
    try:
        data = request.get_json()
        
        if not data or not data.get('tipo_pago'):
            return jsonify({'error': 'El campo tipo_pago es requerido'}), 400
        
        factura, error = OrdenService.crear_factura_desde_orden(orden_cod, data['tipo_pago'])
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Factura creada exitosamente',
            'factura': factura.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@orden_bp.route('/<int:orden_cod>', methods=['DELETE'])
def eliminar_orden(orden_cod):
    """Elimina físicamente una orden"""
    try:
        resultado, error = OrdenService.eliminar_orden(orden_cod)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Orden eliminada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500
    
@orden_bp.route('/<int:orden_cod>/procesar', methods=['POST'])
def procesar_orden(orden_cod):
    """Procesa una orden completada y busca delivery cercano"""
    try:
        data = request.get_json()
        
        if not data or 'latitud_cliente' not in data or 'longitud_cliente' not in data:
            return jsonify({
                'error': 'Se requieren latitud_cliente y longitud_cliente'
            }), 400
        
        # Procesar la orden y buscar delivery cercano
        resultado, error = OrdenService.procesar_orden_completada(
            orden_cod=orden_cod,
            latitud_cliente=data['latitud_cliente'],
            longitud_cliente=data['longitud_cliente']
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        # Extraer los datos del resultado
        orden = resultado['orden']
        delivery_asignado = resultado.get('delivery_asignado')
        notificacion = resultado.get('notificacion')
        
        response_data = {
            'mensaje': 'Orden procesada exitosamente',
            'orden': orden.to_dict(),
            'delivery_asignado': delivery_asignado.to_dict() if delivery_asignado else None,
            'notificacion': notificacion.to_dict() if notificacion else None
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500