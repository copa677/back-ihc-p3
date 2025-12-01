from app.models.orden import Orden
from app.models.detalle_orden import DetalleOrden
from app.models.factura import Factura
from app import db
from sqlalchemy.exc import SQLAlchemyError

class OrdenService:
    
    @staticmethod
    def crear_orden(user_telegram_id, estado='pendiente'):
        """Crea una nueva orden"""
        try:
            orden = Orden(
                user_telegram_id=user_telegram_id,
                estado=estado
            )
            
            db.session.add(orden)
            db.session.commit()
            return orden, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear orden: {str(e)}"
    
    @staticmethod
    def obtener_orden_por_cod(orden_cod):
        """Obtiene una orden por código"""
        try:
            return Orden.query.get(orden_cod)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_ordenes_por_usuario(user_telegram_id):
        """Obtiene todas las órdenes de un usuario"""
        try:
            return Orden.query.filter_by(user_telegram_id=user_telegram_id).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def obtener_todas_ordenes():
        """Obtiene todas las órdenes"""
        try:
            return Orden.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def obtener_ordenes_por_estado(estado):
        """Obtiene órdenes por estado"""
        try:
            return Orden.query.filter_by(estado=estado).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def agregar_detalle_orden(orden_cod, producto_id, cantidad, precio_unitario):
        """Agrega un detalle a la orden"""
        try:
            from app.services.producto_service import ProductoService
            
            # Verificar si el producto existe
            producto = ProductoService.obtener_producto_por_id(producto_id)
            if not producto:
                return None, "Producto no encontrado"
            
            # Verificar si la orden existe
            orden = OrdenService.obtener_orden_por_cod(orden_cod)
            if not orden:
                return None, "Orden no encontrada"
            
            # Crear detalle
            detalle = DetalleOrden(
                orden_cod=orden_cod,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_unitario=precio_unitario
            )
            
            db.session.add(detalle)
            
            # Recalcular total de la orden
            orden.calcular_total()
            db.session.commit()
            
            return detalle, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al agregar detalle a orden: {str(e)}"
    
    @staticmethod
    def actualizar_estado_orden(orden_cod, nuevo_estado):
        """Actualiza el estado de una orden"""
        try:
            orden = OrdenService.obtener_orden_por_cod(orden_cod)
            if not orden:
                return None, "Orden no encontrada"
            
            estados_permitidos = ['pendiente', 'completada', 'cancelada']
            if nuevo_estado not in estados_permitidos:
                return None, f"Estado no válido. Debe ser: {', '.join(estados_permitidos)}"
            
            orden.estado = nuevo_estado
            db.session.commit()
            
            return orden, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar estado de orden: {str(e)}"
    
    @staticmethod
    def actualizar_detalle_orden(detalle_id, nueva_cantidad):
        """Actualiza la cantidad de un detalle"""
        try:
            if nueva_cantidad <= 0:
                return OrdenService.eliminar_detalle_orden(detalle_id)
            
            detalle = DetalleOrden.query.get(detalle_id)
            if not detalle:
                return None, "Detalle no encontrado"
            
            detalle.cantidad = nueva_cantidad
            
            # Recalcular total de la orden
            orden = detalle.orden
            orden.calcular_total()
            db.session.commit()
            
            return detalle, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar detalle: {str(e)}"
    
    @staticmethod
    def eliminar_detalle_orden(detalle_id):
        """Elimina físicamente un detalle de orden"""
        try:
            detalle = DetalleOrden.query.get(detalle_id)
            if not detalle:
                return False, "Detalle no encontrado"
            
            orden = detalle.orden
            db.session.delete(detalle)
            
            # Recalcular total de la orden
            orden.calcular_total()
            db.session.commit()
            
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar detalle: {str(e)}"
    
    @staticmethod
    def eliminar_orden(orden_cod):
        """Elimina físicamente una orden y todos sus detalles"""
        try:
            orden = OrdenService.obtener_orden_por_cod(orden_cod)
            if not orden:
                return False, "Orden no encontrada"
            
            # Los detalles y factura se eliminarán automáticamente por las relaciones cascade
            db.session.delete(orden)
            db.session.commit()
            
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar orden: {str(e)}"
    
    @staticmethod
    def obtener_detalles_orden(orden_cod):
        """Obtiene todos los detalles de una orden"""
        try:
            return DetalleOrden.query.filter_by(orden_cod=orden_cod).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def crear_factura_desde_orden(orden_cod, tipo_pago):
        """Crea una factura a partir de una orden"""
        try:
            orden = OrdenService.obtener_orden_por_cod(orden_cod)
            if not orden:
                return None, "Orden no encontrada"
            
            # Verificar que la orden no tenga ya una factura
            if orden.factura:
                return None, "La orden ya tiene una factura asociada"
            
            # Verificar que la orden tenga detalles
            if not orden.detalles:
                return None, "La orden no tiene detalles"
            
            # Crear factura
            factura = Factura(
                total=orden.total,
                tipo_pago=tipo_pago,
                orden_cod=orden_cod
            )
            
            db.session.add(factura)
            db.session.commit()
            
            return factura, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear factura: {str(e)}"
    
    @staticmethod
    def procesar_orden_completada(orden_cod, latitud_cliente=None, longitud_cliente=None):
        """Procesa una orden completada y busca delivery cercano"""
        try:
            orden = OrdenService.obtener_orden_por_cod(orden_cod)
            if not orden:
                return None, "Orden no encontrada"
            
            # Buscar delivery más cercano si se proporcionan coordenadas
            if latitud_cliente and longitud_cliente:
                from app.services.notificacion_service import NotificacionService
                
                delivery_cercano, error = NotificacionService.encontrar_delivery_cercano(
                    latitud_cliente, longitud_cliente
                )
                
                if error or not delivery_cercano:
                    return None, "No se encontró ningún delivery disponible"
                
                # Crear notificación para el delivery
                notificacion, error = NotificacionService.crear_notificacion_orden(
                    delivery_cercano.id, orden_cod
                )
                
                if error:
                    return None, error
                
                return {
                    'orden': orden,
                    'delivery_asignado': delivery_cercano,
                    'notificacion': notificacion
                }, None
            
            return orden, None
            
        except Exception as e:
            return None, f"Error al procesar orden: {str(e)}"    
        
    @staticmethod
    def crear_orden_con_asignacion_automatica(user_telegram_id, restaurant_lat, restaurant_lon, estado='pendiente'):
        """
        Crea una nueva orden y la asigna automáticamente al delivery más cercano.
        Inicializa el registro de rechazos para esta orden.
        """
        from app.utils.distance_calculator import find_closest_delivery, assign_order_to_closest_delivery
        from app.utils.rechazos_manager import inicializar_rechazos_orden
        
        try:
            # Primero crear la orden
            orden, error = OrdenService.crear_orden(user_telegram_id, estado)
            if error:
                return None, None, None, error
            
            # INICIALIZAR registro de rechazos para esta nueva orden
            inicializar_rechazos_orden(orden.cod)
            
            # Asignar automáticamente al delivery más cercano
            success, message, delivery = assign_order_to_closest_delivery(
                orden.cod, restaurant_lat, restaurant_lon
            )
            
            if not success:
                return orden, None, message, None
            
            return orden, delivery, f"Orden {orden.cod} asignada a {delivery.username}", None
            
        except Exception as e:
            db.session.rollback()
            return None, None, None, f"Error al crear orden con asignación automática: {str(e)}"