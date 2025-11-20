from flask import Blueprint, request, jsonify
from app.services.carrito_service import CarritoService

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/usuario/<int:usuario_id>', methods=['POST'])
def crear_carrito(usuario_id):
    """Crea un nuevo carrito para un usuario"""
    try:
        carrito, error = CarritoService.crear_carrito(usuario_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Carrito creado exitosamente',
            'carrito': carrito.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@carrito_bp.route('/usuario/<int:usuario_id>', methods=['GET'])
def obtener_carrito_usuario(usuario_id):
    """Obtiene el carrito activo de un usuario"""
    try:
        carrito = CarritoService.obtener_carrito_por_usuario(usuario_id)
        if not carrito:
            return jsonify({'error': 'Carrito no encontrado'}), 404
        
        # Obtener items del carrito
        items = CarritoService.obtener_items_carrito(carrito.id)
        
        return jsonify({
            'carrito': carrito.to_dict(),
            'items': [item.to_dict() for item in items]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@carrito_bp.route('/<int:carrito_id>/agregar-item', methods=['POST'])
def agregar_item_carrito(carrito_id):
    """Agrega un item al carrito"""
    try:
        data = request.get_json()
        
        if not data or not data.get('producto_id'):
            return jsonify({'error': 'El campo producto_id es requerido'}), 400
        
        cantidad = data.get('cantidad', 1)
        
        item, error = CarritoService.agregar_item_carrito(carrito_id, data['producto_id'], cantidad)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Item agregado al carrito exitosamente',
            'item': item.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@carrito_bp.route('/item/<int:item_id>', methods=['PUT'])
def actualizar_cantidad_item(item_id):
    """Actualiza la cantidad de un item en el carrito"""
    try:
        data = request.get_json()
        
        if not data or data.get('cantidad') is None:
            return jsonify({'error': 'El campo cantidad es requerido'}), 400
        
        item, error = CarritoService.actualizar_cantidad_item(item_id, data['cantidad'])
        if error:
            return jsonify({'error': error}), 400
        
        if item:  # Si se actualizó la cantidad
            return jsonify({
                'mensaje': 'Cantidad actualizada exitosamente',
                'item': item.to_dict()
            }), 200
        else:  # Si se eliminó el item (cantidad = 0)
            return jsonify({
                'mensaje': 'Item eliminado del carrito'
            }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@carrito_bp.route('/item/<int:item_id>', methods=['DELETE'])
def eliminar_item_carrito(item_id):
    """Elimina un item del carrito"""
    try:
        resultado, error = CarritoService.eliminar_item_carrito(item_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Item eliminado del carrito exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@carrito_bp.route('/<int:carrito_id>/vaciar', methods=['DELETE'])
def vaciar_carrito(carrito_id):
    """Vacía todos los items del carrito"""
    try:
        resultado, error = CarritoService.vaciar_carrito(carrito_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Carrito vaciado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500
    
@carrito_bp.route('/<int:carrito_id>', methods=['DELETE'])
def eliminar_carrito(carrito_id):
    """Elimina físicamente un carrito y todos sus items"""
    try:
        resultado, error = CarritoService.eliminar_carrito(carrito_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Carrito eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500
    
# Agregar esta ruta al archivo carrito.py
@carrito_bp.route('/', methods=['GET'])
def obtener_todos_carritos():
    """Obtiene todos los carritos"""
    try:
        carritos = CarritoService.obtener_todos_carritos()
        
        carritos_con_items = []
        for carrito in carritos:
            items = CarritoService.obtener_items_carrito(carrito.id)
            carrito_dict = carrito.to_dict()
            carrito_dict['items'] = [item.to_dict() for item in items]
            carritos_con_items.append(carrito_dict)
        
        return jsonify({
            'carritos': carritos_con_items
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500