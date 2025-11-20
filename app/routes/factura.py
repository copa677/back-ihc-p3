from flask import Blueprint, request, jsonify
from app.services.factura_service import FacturaService

factura_bp = Blueprint('factura', __name__)

@factura_bp.route('/', methods=['GET'])
def obtener_todas_facturas():
    """Obtiene todas las facturas"""
    try:
        facturas = FacturaService.obtener_todas_facturas()
        
        return jsonify({
            'facturas': [factura.to_dict() for factura in facturas]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@factura_bp.route('/<int:factura_cod>', methods=['GET'])
def obtener_factura(factura_cod):
    """Obtiene una factura específica por código"""
    try:
        factura = FacturaService.obtener_factura_por_cod(factura_cod)
        if not factura:
            return jsonify({'error': 'Factura no encontrada'}), 404
        
        return jsonify({
            'factura': factura.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@factura_bp.route('/orden/<int:orden_cod>', methods=['GET'])
def obtener_factura_por_orden(orden_cod):
    """Obtiene la factura de una orden específica"""
    try:
        factura = FacturaService.obtener_facturas_por_orden(orden_cod)
        if not factura:
            return jsonify({'error': 'Factura no encontrada para esta orden'}), 404
        
        return jsonify({
            'factura': factura.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@factura_bp.route('/estado/<string:estado>', methods=['GET'])
def obtener_facturas_por_estado(estado):
    """Obtiene facturas por estado"""
    try:
        facturas = FacturaService.obtener_facturas_por_estado(estado)
        
        return jsonify({
            'facturas': [factura.to_dict() for factura in facturas],
            'estado': estado
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@factura_bp.route('/<int:factura_cod>/estado', methods=['PUT'])
def actualizar_estado_factura(factura_cod):
    """Actualiza el estado de una factura"""
    try:
        data = request.get_json()
        
        if not data or not data.get('estado'):
            return jsonify({'error': 'El campo estado es requerido'}), 400
        
        factura, error = FacturaService.actualizar_estado_factura(factura_cod, data['estado'])
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Estado de factura actualizado exitosamente',
            'factura': factura.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@factura_bp.route('/<int:factura_cod>', methods=['DELETE'])
def eliminar_factura(factura_cod):
    """Elimina físicamente una factura"""
    try:
        resultado, error = FacturaService.eliminar_factura(factura_cod)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Factura eliminada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500