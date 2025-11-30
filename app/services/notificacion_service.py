from app.models.notificacion import Notificacion
from app.models.tracking_orden import TrackingOrden
from app.models.user_delivery import UserDelivery
from app import db
from sqlalchemy.exc import SQLAlchemyError
import math

class NotificacionService:
    
    @staticmethod
    def calcular_distancia(lat1, lon1, lat2, lon2):
        """Calcula distancia entre dos coordenadas (fórmula haversine)"""
        R = 6371  # Radio de la Tierra en km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distancia = R * c
        
        return distancia

    @staticmethod
    def encontrar_delivery_cercano(latitud_cliente, longitud_cliente):
        """Encuentra el delivery más cercano usando coordenadas"""
        try:
            deliveries = UserDelivery.query.filter_by(esta_activo=True).all()
            
            delivery_cercano = None
            distancia_minima = float('inf')
            
            for delivery in deliveries:
                if delivery.latitud and delivery.longitud:
                    distancia = NotificacionService.calcular_distancia(
                        float(latitud_cliente), float(longitud_cliente),
                        float(delivery.latitud), float(delivery.longitud)
                    )
                    if distancia < distancia_minima:
                        distancia_minima = distancia
                        delivery_cercano = delivery
            
            return delivery_cercano, None
            
        except Exception as e:
            return None, f"Error al buscar delivery: {str(e)}"

    @staticmethod
    def crear_notificacion_orden(user_delivery_id, orden_cod):
        """Crea notificación de nueva orden para delivery"""
        try:
            notificacion = Notificacion(
                user_delivery_id=user_delivery_id,
                orden_cod=orden_cod,
                tipo='nueva_orden',
                mensaje=f'Nueva orden #{orden_cod} disponible para entrega',
                estado='pendiente'
            )
            
            db.session.add(notificacion)
            db.session.commit()
            return notificacion, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear notificación: {str(e)}"

    @staticmethod
    def obtener_notificaciones_pendientes(user_delivery_id):
        """Obtiene notificaciones pendientes para un delivery"""
        try:
            return Notificacion.query.filter_by(
                user_delivery_id=user_delivery_id, 
                visto=False
            ).all()
        except SQLAlchemyError:
            return []

    @staticmethod
    def responder_notificacion(notificacion_id, respuesta):
        """Procesa respuesta del delivery (aceptar/rechazar)"""
        try:
            notificacion = Notificacion.query.get(notificacion_id)
            if not notificacion:
                return None, "Notificación no encontrada"
            
            if respuesta == 'aceptar':
                # Crear registro en tracking
                tracking = TrackingOrden(
                    orden_cod=notificacion.orden_cod,
                    user_delivery_id=notificacion.user_delivery_id,
                    estado='asignada'
                )
                db.session.add(tracking)
                
                # Actualizar estado de la orden
                from app.services.orden_service import OrdenService
                orden, error = OrdenService.actualizar_estado_orden(
                    notificacion.orden_cod, 'asignada'
                )
                if error:
                    return None, error
                
                notificacion.estado = 'aceptada'
                mensaje = 'Orden aceptada correctamente'
                
            elif respuesta == 'rechazar':
                notificacion.estado = 'rechazada'
                notificacion.visto = True
                
                # ✅ NUEVO: Re-asignar automáticamente a otro delivery
                reasignacion_exitosa = NotificacionService.reasignar_orden(
                    notificacion.orden_cod, 
                    notificacion.user_delivery_id  # Excluir al que rechazó
                )
                
                if reasignacion_exitosa:
                    mensaje = 'Orden rechazada. Se ha asignado a otro delivery.'
                else:
                    mensaje = 'Orden rechazada. No hay más deliveries disponibles.'
                    
            db.session.commit()
            return notificacion, mensaje
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al procesar respuesta: {str(e)}"
        
    @staticmethod
    def reasignar_orden(orden_cod, delivery_excluido_id):
        """Re-asigna la orden a otro delivery disponible"""
        try:
            # Buscar orden para obtener coordenadas del cliente
            from app.services.orden_service import OrdenService
            from app.models.datos_envio import DatosEnvio

            orden = OrdenService.obtener_orden_por_cod(orden_cod)
            
            if not orden:
                return False
            
            # Obtener datos de envío del cliente
            datos_envio = DatosEnvio.query.filter_by(
                user_telegram_id=orden.user_telegram_id
            ).first()
            
            if not datos_envio or not datos_envio.latitud or not datos_envio.longitud:
                return False
            
            # Buscar otro delivery (excluyendo al que rechazó)
            deliveries = UserDelivery.query.filter(
                UserDelivery.esta_activo == True,
                UserDelivery.id != delivery_excluido_id,
                UserDelivery.latitud.isnot(None),
                UserDelivery.longitud.isnot(None)
            ).all()
            
            if not deliveries:
                return False
            
            # Encontrar el más cercano entre los disponibles
            delivery_cercano = None
            distancia_minima = float('inf')
            
            for delivery in deliveries:
                distancia = NotificacionService.calcular_distancia(
                    float(datos_envio.latitud), float(datos_envio.longitud),
                    float(delivery.latitud), float(delivery.longitud)
                )
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    delivery_cercano = delivery
            
            if delivery_cercano:
                # Crear nueva notificación para el siguiente delivery
                notificacion = Notificacion(
                    user_delivery_id=delivery_cercano.id,
                    orden_cod=orden_cod,
                    tipo='nueva_orden',
                    mensaje=f'Nueva orden #{orden_cod} disponible para entrega (reasignada)',
                    estado='pendiente'
                )
                db.session.add(notificacion)
                return True
            
            return False
            
        except Exception as e:
            print(f"Error en reasignación: {str(e)}")
            return False