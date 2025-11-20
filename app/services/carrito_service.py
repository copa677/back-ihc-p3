from app.models.carrito import Carrito
from app.models.item_carrito import ItemCarrito
from app import db
from sqlalchemy.exc import SQLAlchemyError

class CarritoService:
    
    @staticmethod
    def crear_carrito(usuario_id):
        """Crea un nuevo carrito para un usuario"""
        try:
            carrito = Carrito(usuario_id=usuario_id)
            db.session.add(carrito)
            db.session.commit()
            return carrito, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear carrito: {str(e)}"
    
    @staticmethod
    def obtener_carrito_por_usuario(usuario_id):
        """Obtiene el carrito de un usuario"""
        try:
            return Carrito.query.filter_by(usuario_id=usuario_id).first()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_carrito_por_id(carrito_id):
        """Obtiene un carrito por ID"""
        try:
            return Carrito.query.get(carrito_id)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_todos_carritos():
        """Obtiene todos los carritos"""
        try:
            return Carrito.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def agregar_item_carrito(carrito_id, producto_id, cantidad=1):
        """Agrega un item al carrito"""
        try:
            from app.services.producto_service import ProductoService
            
            # Verificar si el producto existe
            producto = ProductoService.obtener_producto_por_id(producto_id)
            if not producto:
                return None, "Producto no encontrado"
            
            # Verificar si el carrito existe
            carrito = CarritoService.obtener_carrito_por_id(carrito_id)
            if not carrito:
                return None, "Carrito no encontrado"
            
            # Verificar si el item ya existe en el carrito
            item_existente = ItemCarrito.query.filter_by(
                carrito_id=carrito_id, 
                producto_id=producto_id
            ).first()
            
            if item_existente:
                # Actualizar cantidad si ya existe
                item_existente.cantidad += cantidad
                item = item_existente
            else:
                # Crear nuevo item
                item = ItemCarrito(
                    name=producto.name,
                    precio_unitario=producto.price,
                    cantidad=cantidad,
                    carrito_id=carrito_id,
                    producto_id=producto_id
                )
                db.session.add(item)
            
            # Recalcular total del carrito
            carrito.calcular_total()
            db.session.commit()
            
            return item, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al agregar item al carrito: {str(e)}"
    
    @staticmethod
    def actualizar_cantidad_item(item_id, nueva_cantidad):
        """Actualiza la cantidad de un item en el carrito"""
        try:
            if nueva_cantidad <= 0:
                return CarritoService.eliminar_item_carrito(item_id)
            
            item = ItemCarrito.query.get(item_id)
            if not item:
                return None, "Item no encontrado"
            
            item.cantidad = nueva_cantidad
            
            # Recalcular total del carrito
            carrito = item.carrito
            carrito.calcular_total()
            db.session.commit()
            
            return item, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar cantidad: {str(e)}"
    
    @staticmethod
    def eliminar_item_carrito(item_id):
        """Elimina físicamente un item del carrito"""
        try:
            item = ItemCarrito.query.get(item_id)
            if not item:
                return False, "Item no encontrado"
            
            carrito = item.carrito
            db.session.delete(item)
            
            # Recalcular total del carrito
            carrito.calcular_total()
            db.session.commit()
            
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar item: {str(e)}"
    
    @staticmethod
    def eliminar_carrito(carrito_id):
        """Elimina físicamente un carrito y todos sus items"""
        try:
            carrito = CarritoService.obtener_carrito_por_id(carrito_id)
            if not carrito:
                return False, "Carrito no encontrado"
            
            # Los items se eliminarán automáticamente por la relación cascade
            db.session.delete(carrito)
            db.session.commit()
            
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar carrito: {str(e)}"
    
    @staticmethod
    def obtener_items_carrito(carrito_id):
        """Obtiene todos los items de un carrito"""
        try:
            return ItemCarrito.query.filter_by(carrito_id=carrito_id).all()
        except SQLAlchemyError:
            return []