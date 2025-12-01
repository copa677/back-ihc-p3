from app.models.tracking_orden import TrackingOrden
from app import db
from sqlalchemy.exc import SQLAlchemyError

class TrackingService:
    
    @staticmethod
    def crear_tracking(orden_cod, user_delivery_id, estado, latitud=None, longitud=None, comentario=None):
        """
        Crea un nuevo registro de tracking.
        
        Args:
            orden_cod: Código de la orden
            user_delivery_id: ID del delivery asignado
            estado: Estado del tracking
            latitud, longitud: Coordenadas GPS (opcionales)
            comentario: Observaciones (opcionales)
        """
        try:
            tracking = TrackingOrden(
                orden_cod=orden_cod,
                user_delivery_id=user_delivery_id,
                estado=estado,
                latitud=latitud,
                longitud=longitud,
                comentario=comentario
            )
            
            db.session.add(tracking)
            db.session.commit()
            return tracking, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear tracking: {str(e)}"

    @staticmethod
    def obtener_tracking_por_id(tracking_id):
        """Obtiene un tracking específico por su ID"""
        try:
            return TrackingOrden.query.get(tracking_id)
        except SQLAlchemyError:
            return None

    @staticmethod
    def actualizar_tracking(tracking_id, datos_actualizados):
        """
        Actualiza un tracking existente.
        
        Args:
            tracking_id: ID del tracking a actualizar
            datos_actualizados: Diccionario con campos a actualizar
        """
        try:
            tracking = TrackingOrden.query.get(tracking_id)
            if not tracking:
                return None, "Tracking no encontrado"
            
            # Campos que se pueden actualizar
            if 'estado' in datos_actualizados:
                tracking.estado = datos_actualizados['estado']
            
            if 'latitud' in datos_actualizados:
                tracking.latitud = datos_actualizados['latitud']
            
            if 'longitud' in datos_actualizados:
                tracking.longitud = datos_actualizados['longitud']
            
            if 'comentario' in datos_actualizados:
                tracking.comentario = datos_actualizados['comentario']
            
            # fecha_actualizacion se actualiza automáticamente por onupdate
            
            db.session.commit()
            return tracking, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar tracking: {str(e)}"

    @staticmethod
    def eliminar_tracking(tracking_id):
        """Elimina físicamente un registro de tracking"""
        try:
            tracking = TrackingOrden.query.get(tracking_id)
            if not tracking:
                return False, "Tracking no encontrado"
            
            db.session.delete(tracking)
            db.session.commit()
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar tracking: {str(e)}"

    @staticmethod
    def obtener_historial_por_delivery(user_delivery_id, limit=None):
        """
        Obtiene el historial de tracking de un delivery específico.
        
        Args:
            user_delivery_id: ID del delivery
            limit: Límite de resultados (opcional)
        """
        try:
            query = TrackingOrden.query.filter_by(
                user_delivery_id=user_delivery_id
            ).order_by(
                TrackingOrden.fecha_creacion.desc()
            )
            
            if limit:
                query = query.limit(limit)
            
            return query.all()
        except SQLAlchemyError:
            return []

    @staticmethod
    def obtener_trackings_por_orden(orden_cod):
        """Obtiene todos los trackings de una orden específica"""
        try:
            return TrackingOrden.query.filter_by(
                orden_cod=orden_cod
            ).order_by(
                TrackingOrden.fecha_creacion.desc()
            ).all()
        except SQLAlchemyError:
            return []