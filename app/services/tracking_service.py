from app.models.tracking_orden import TrackingOrden
from app import db
from sqlalchemy.exc import SQLAlchemyError

class TrackingService:
    
    @staticmethod
    def crear_tracking(orden_cod, user_delivery_id, estado='asignada'):
        """Crea un nuevo registro de tracking"""
        try:
            tracking = TrackingOrden(
                orden_cod=orden_cod,
                user_delivery_id=user_delivery_id,
                estado=estado
            )
            
            db.session.add(tracking)
            db.session.commit()
            return tracking, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear tracking: {str(e)}"

    @staticmethod
    def obtener_tracking_por_orden(orden_cod):
        """Obtiene el tracking de una orden específica"""
        try:
            return TrackingOrden.query.filter_by(orden_cod=orden_cod).first()
        except SQLAlchemyError:
            return None

    @staticmethod
    def actualizar_tracking(orden_cod, datos_actualizados):
        """Actualiza el estado y ubicación del tracking"""
        try:
            tracking = TrackingOrden.query.filter_by(orden_cod=orden_cod).first()
            if not tracking:
                return None, "Tracking no encontrado"
            
            if 'estado' in datos_actualizados:
                tracking.estado = datos_actualizados['estado']
            
            if 'latitud' in datos_actualizados:
                tracking.latitud = datos_actualizados['latitud']
            
            if 'longitud' in datos_actualizados:
                tracking.longitud = datos_actualizados['longitud']
            
            if 'comentario' in datos_actualizados:
                tracking.comentario = datos_actualizados['comentario']
            
            db.session.commit()
            return tracking, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar tracking: {str(e)}"

    @staticmethod
    def obtener_historial_tracking(orden_cod):
        """Obtiene todo el historial de tracking de una orden"""
        try:
            return TrackingOrden.query.filter_by(orden_cod=orden_cod).order_by(
                TrackingOrden.fecha_creacion.desc()
            ).all()
        except SQLAlchemyError:
            return []