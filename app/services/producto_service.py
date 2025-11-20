from app.models.producto import Producto
from app import db
from sqlalchemy.exc import SQLAlchemyError

class ProductoService:
    
    @staticmethod
    def crear_producto(datos):
        """Crea un nuevo producto"""
        try:
            producto = Producto(
                name=datos['name'],
                price=datos['price'],
                image=datos.get('image'),
                category=datos['category']
            )
            
            db.session.add(producto)
            db.session.commit()
            return producto, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear producto: {str(e)}"
    
    @staticmethod
    def obtener_producto_por_id(producto_id):
        """Obtiene un producto por ID"""
        try:
            return Producto.query.get(producto_id)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_todos_productos():
        """Obtiene todos los productos activos"""
        try:
            return Producto.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def obtener_productos_por_categoria(categoria):
        """Obtiene productos por categoría"""
        try:
            return Producto.query.filter_by(category=categoria).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def actualizar_producto(producto_id, datos_actualizados):
        """Actualiza un producto"""
        try:
            producto = Producto.query.get(producto_id)
            if not producto:
                return None, "Producto no encontrado"
            
            campos_permitidos = ['name', 'price', 'image', 'category', 'esta_activo']
            
            for campo in campos_permitidos:
                if campo in datos_actualizados:
                    setattr(producto, campo, datos_actualizados[campo])
            
            db.session.commit()
            return producto, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar producto: {str(e)}"
    
    @staticmethod
    def eliminar_producto(producto_id):
        """Elimina físicamente un producto"""
        try:
            producto = Producto.query.get(producto_id)
            if not producto:
                return False, "Producto no encontrado"
            
            db.session.delete(producto)
            db.session.commit()
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar producto: {str(e)}"