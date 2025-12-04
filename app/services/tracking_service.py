from app.models.tracking_orden import TrackingOrden
from app.models.orden import Orden
from app.models.user_telgram import UserTelegram
from app.models.user_delivery import UserDelivery
from app.models.datos_envio import DatosEnvio
from app import db
from sqlalchemy.exc import SQLAlchemyError
import requests
import os

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
            # Buscar el user_delivery y cambiar su id_orden a null
            user_delivery = UserDelivery.query.get(user_delivery_id)
            if user_delivery:
                user_delivery.id_orden = None
            
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
        Obtiene el historial de tracking de un delivery específico con datos de envío.
        
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
            
            trackings = query.all()
            
            # Crear resultado con información adicional de datos de envío
            resultado = []
            for tracking in trackings:
                tracking_dict = tracking.to_dict()
                
                # Obtener datos de envío de la orden
                datos_envio = DatosEnvio.query.filter_by(orden_id=tracking.orden_cod).first()
                
                # Agregar datos de envío si existen
                if datos_envio:
                    tracking_dict['datos_envio'] = {
                        'nombre_completo': datos_envio.nombre_completo,
                        'telefono': datos_envio.telefono,
                        'comentario': datos_envio.comentario
                    }
                else:
                    tracking_dict['datos_envio'] = None
                
                resultado.append(tracking_dict)
            
            return resultado
        except SQLAlchemyError:
            return []

    @staticmethod
    def obtener_trackings_por_orden(orden_cod):
        """Obtiene todos los trackings de una orden específica con datos de envío"""
        try:
            trackings = TrackingOrden.query.filter_by(
                orden_cod=orden_cod
            ).order_by(
                TrackingOrden.fecha_creacion.desc()
            ).all()
            
            # Obtener datos de envío de la orden
            datos_envio = DatosEnvio.query.filter_by(orden_id=orden_cod).first()
            
            # Crear resultado con información adicional
            resultado = []
            for tracking in trackings:
                tracking_dict = tracking.to_dict()
                
                # Agregar datos de envío si existen
                if datos_envio:
                    tracking_dict['datos_envio'] = {
                        'nombre_completo': datos_envio.nombre_completo,
                        'telefono': datos_envio.telefono,
                        'comentario': datos_envio.comentario
                    }
                else:
                    tracking_dict['datos_envio'] = None
                
                resultado.append(tracking_dict)
            
            return resultado
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def enviar_notificacion_telegram(tracking_id, estado):
        """
        Envía una notificación al usuario de Telegram cuando cambia el estado del tracking.
        
        Args:
            tracking_id: ID del tracking
            estado: Nuevo estado del tracking
        
        Returns:
            tuple: (success: bool, error: str or None)
        """
        try:
            # Obtener el tracking
            tracking = TrackingOrden.query.get(tracking_id)
            if not tracking:
                return False, "Tracking no encontrado"
            
            # Obtener la orden asociada
            orden = Orden.query.get(tracking.orden_cod)
            if not orden:
                return False, "Orden no encontrada"
            
            # Obtener el usuario de Telegram
            user_telegram = UserTelegram.query.get(orden.user_telegram_id)
            if not user_telegram:
                return False, "Usuario de Telegram no encontrado"
            
            # Obtener el token del bot desde las variables de entorno
            bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
            if not bot_token:
                return False, "Token del bot de Telegram no configurado en variables de entorno"
            
            # Definir mensajes según el estado
            mensajes = {
                'asignada': f'🚚 ¡Tu pedido #{orden.cod} ha sido asignado a un delivery!\n\nEstaremos recogiendo tu pedido pronto.',
                'recogiendo': f'📦 El delivery está recogiendo tu pedido #{orden.cod}\n\n¡Ya casi estamos en camino!',
                'en_camino': f'🛵 ¡Tu pedido #{orden.cod} está en camino!\n\nLlegará pronto a tu destino.',
                'entregada': f'✅ ¡Tu pedido #{orden.cod} ha sido entregado!\n\nGracias por tu preferencia. 🎉',
                'cancelada': f'❌ Tu pedido #{orden.cod} ha sido cancelado.\n\nSi tienes preguntas, contáctanos.'
            }
            
            mensaje = mensajes.get(estado, f'Estado actualizado: {estado}')
            
            # Enviar mensaje a Telegram
            url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
            payload = {
                'chat_id': user_telegram.chat_id,
                'text': mensaje,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return True, None
            else:
                return False, f"Error en API de Telegram: {response.text}"
                
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión con Telegram: {str(e)}"
        except Exception as e:
            return False, f"Error al enviar notificación: {str(e)}"