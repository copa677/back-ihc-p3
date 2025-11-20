from app.models.datos_pago import DatosPago
from app import db
from sqlalchemy.exc import SQLAlchemyError

class DatosPagoService:
    
    @staticmethod
    def crear_datos_pago(datos):
        """Crea nuevos datos de pago"""
        try:
            datos_pago = DatosPago(
                numero_tarjeta=datos['numero_tarjeta'],
                fecha_expiracion_tarjeta=datos['fecha_expiracion_tarjeta'],
                nombre_propietario=datos['nombre_propietario'],
                codigo_seguridad=datos['codigo_seguridad'],
                pais=datos['pais'],
                codigo_postal=datos['codigo_postal'],
                usuario_id=datos['usuario_id']
            )
            
            db.session.add(datos_pago)
            db.session.commit()
            return datos_pago, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al crear datos de pago: {str(e)}"
    
    @staticmethod
    def obtener_datos_pago_por_id(datos_pago_id):
        """Obtiene datos de pago por ID"""
        try:
            return DatosPago.query.get(datos_pago_id)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_datos_pago_por_usuario(usuario_id):
        """Obtiene todos los datos de pago de un usuario"""
        try:
            return DatosPago.query.filter_by(usuario_id=usuario_id).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def obtener_todos_datos_pago():
        """Obtiene todos los datos de pago"""
        try:
            return DatosPago.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def actualizar_datos_pago(datos_pago_id, datos_actualizados):
        """Actualiza datos de pago"""
        try:
            datos_pago = DatosPago.query.get(datos_pago_id)
            if not datos_pago:
                return None, "Datos de pago no encontrados"
            
            campos_permitidos = ['numero_tarjeta', 'fecha_expiracion_tarjeta', 
                               'nombre_propietario', 'codigo_seguridad', 'pais', 'codigo_postal']
            
            for campo in campos_permitidos:
                if campo in datos_actualizados:
                    setattr(datos_pago, campo, datos_actualizados[campo])
            
            db.session.commit()
            return datos_pago, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar datos de pago: {str(e)}"
    
    @staticmethod
    def eliminar_datos_pago(datos_pago_id):
        """Elimina físicamente los datos de pago"""
        try:
            datos_pago = DatosPago.query.get(datos_pago_id)
            if not datos_pago:
                return False, "Datos de pago no encontrados"
            
            db.session.delete(datos_pago)
            db.session.commit()
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar datos de pago: {str(e)}"