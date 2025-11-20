from flask import Blueprint, request, jsonify
from app.services.producto_service import ProductoService

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['POST'])
def crear_producto():
    """Crea un nuevo producto"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        campos_requeridos = ['name', 'price', 'category']
        for campo in campos_requeridos:
            if not data.get(campo):
                return jsonify({'error': f'El campo {campo} es requerido'}), 400
        
        producto, error = ProductoService.crear_producto(data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Producto creado exitosamente',
            'producto': producto.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@productos_bp.route('/', methods=['GET'])
def obtener_productos():
    """Obtiene todos los productos activos"""
    try:
        productos = ProductoService.obtener_todos_productos()
        
        return jsonify({
            'productos': [producto.to_dict() for producto in productos]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@productos_bp.route('/categoria/<string:categoria>', methods=['GET'])
def obtener_productos_por_categoria(categoria):
    """Obtiene productos por categoría"""
    try:
        productos = ProductoService.obtener_productos_por_categoria(categoria)
        
        return jsonify({
            'productos': [producto.to_dict() for producto in productos],
            'categoria': categoria
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@productos_bp.route('/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    """Obtiene un producto específico por ID"""
    try:
        producto = ProductoService.obtener_producto_por_id(producto_id)
        if not producto:
            return jsonify({'error': 'Producto no encontrado'}), 404
        
        return jsonify({
            'producto': producto.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@productos_bp.route('/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    """Actualiza un producto"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se proporcionaron datos para actualizar'}), 400
        
        producto_actualizado, error = ProductoService.actualizar_producto(producto_id, data)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Producto actualizado exitosamente',
            'producto': producto_actualizado.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500

@productos_bp.route('/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    """Elimina físicamente un producto"""
    try:
        resultado, error = ProductoService.eliminar_producto(producto_id)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'mensaje': 'Producto eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Error en el servidor: {str(e)}'}), 500