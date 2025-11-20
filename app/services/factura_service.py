from app.models.factura import Factura
from app import db
from sqlalchemy.exc import SQLAlchemyError

class FacturaService:
    
    @staticmethod
    def obtener_factura_por_cod(factura_cod):
        """Obtiene una factura por código"""
        try:
            return Factura.query.get(factura_cod)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_facturas_por_orden(orden_cod):
        """Obtiene la factura de una orden"""
        try:
            return Factura.query.filter_by(orden_cod=orden_cod).first()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def obtener_todas_facturas():
        """Obtiene todas las facturas"""
        try:
            return Factura.query.all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def obtener_facturas_por_estado(estado):
        """Obtiene facturas por estado"""
        try:
            return Factura.query.filter_by(estado=estado).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def actualizar_estado_factura(factura_cod, nuevo_estado):
        """Actualiza el estado de una factura"""
        try:
            factura = FacturaService.obtener_factura_por_cod(factura_cod)
            if not factura:
                return None, "Factura no encontrada"
            
            estados_permitidos = ['pendiente', 'pagada', 'cancelada']
            if nuevo_estado not in estados_permitidos:
                return None, f"Estado no válido. Debe ser: {', '.join(estados_permitidos)}"
            
            factura.estado = nuevo_estado
            db.session.commit()
            
            return factura, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Error al actualizar estado de factura: {str(e)}"
    
    @staticmethod
    def eliminar_factura(factura_cod):
        """Elimina físicamente una factura"""
        try:
            factura = FacturaService.obtener_factura_por_cod(factura_cod)
            if not factura:
                return False, "Factura no encontrada"
            
            db.session.delete(factura)
            db.session.commit()
            
            return True, None
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error al eliminar factura: {str(e)}"