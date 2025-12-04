from app.models.datos_envio import DatosEnvio
from app import db
from sqlalchemy.exc import SQLAlchemyError

class DatosEnvioService:
    
    @staticmethod
    def crear_datos_envio(datos):
        """Crea nuevos datos de envío"""
        try:
            datos_envio = DatosEnvio(
                latitud=datos['latitud'],
                longitud=datos['longitud'],
                ciudad=datos['ciudad'],
                region=datos['region'],
                codigo_postal=datos['codigo_postal'],
                nombre_completo=datos['nombre_completo'],
                telefono=datos['telefono'],
                comentario=datos.get('comentario'),
                user_telegram_id=datos['user_telegram_id'],
                orden_id=datos['orden_id']
            )
            
            db.session.add(datos_envio)
            db.session.commit()
            return datos_envio, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear datos de envío: {str(e)}"
    
    @staticmethod
    def obtener_datos_envio_por_id(datos_envio_id):
        """Obtiene datos de envío por ID"""
        try:
            return DatosEnvio.query.get(datos_envio_id)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_datos_envio_por_usuario(user_telegram_id):
        """Obtiene todos los datos de envío de un usuario"""
        try:
            return DatosEnvio.query.filter_by(user_telegram_id=user_telegram_id).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def obtener_todos_datos_envio():
        """Obtiene todos los datos de envío"""
        try:
            return DatosEnvio.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def actualizar_datos_envio(datos_envio_id, datos_actualizados):
        """Actualiza datos de envío"""
        try:
            datos_envio = DatosEnvio.query.get(datos_envio_id)
            if not datos_envio:
                return None, "Datos de envío no encontrados"
            
            campos_permitidos = ['direccion1', 'direccion2', 'ciudad', 'region', 
                               'codigo_postal', 'nombre_completo', 'telefono', 'comentario']
            
            for campo in campos_permitidos:
                if campo in datos_actualizados:
                    setattr(datos_envio, campo, datos_actualizados[campo])
            
            db.session.commit()
            return datos_envio, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar datos de envío: {str(e)}"
    
    @staticmethod
    def eliminar_datos_envio(datos_envio_id):
        """Elimina físicamente los datos de envío"""
        try:
            datos_envio = DatosEnvio.query.get(datos_envio_id)
            if not datos_envio:
                return False, "Datos de envío no encontrados"
            
            db.session.delete(datos_envio)
            db.session.commit()
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar datos de envío: {str(e)}"
        
    @staticmethod
    def obtener_ubicacion_por_orden(orden_id):
        """
        Obtiene SOLO la latitud y longitud de los datos de envío de una orden.
        
        Args:
            orden_id: ID de la orden
        
        Returns:
            Dict con latitud y longitud o None si no existe
        """
        try:
            datos_envio = DatosEnvio.query.filter_by(orden_id=orden_id).first()
            
            if not datos_envio:
                return None
            
            return {
                'latitud': float(datos_envio.latitud) if datos_envio.latitud else None,
                'longitud': float(datos_envio.longitud) if datos_envio.longitud else None,
                'direccion_completa': {
                    'ciudad': datos_envio.ciudad,
                    'region': datos_envio.region,
                    'codigo_postal': datos_envio.codigo_postal
                },
                'contacto': {
                    'nombre_completo': datos_envio.nombre_completo,
                    'telefono': datos_envio.telefono,
                    'comentario': datos_envio.comentario
                },
                'orden_id': orden_id,
                'datos_envio_id': datos_envio.id
            }
        except SQLAlchemyError:
            return None