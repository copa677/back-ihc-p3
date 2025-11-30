from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class DetalleOrden(db.Model):
    __tablename__ = 'detalle_orden'
    
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    fecha_agregacion = db.Column(db.DateTime, default=lambda: get_bolivia_time())
    
    # Foreign keys
    orden_cod = db.Column(db.Integer, db.ForeignKey('orden.cod'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)

    @property
    def subtotal(self):
        """Calcula el subtotal del detalle"""
        return self.precio_unitario * self.cantidad

    def to_dict(self):
        # Convertir a zona horaria de Bolivia para la respuesta
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        fecha_agregacion_bolivia = self.fecha_agregacion
        
        # Si la fecha está en UTC, convertirla a Bolivia
        if self.fecha_agregacion.tzinfo is None:
            fecha_agregacion_bolivia = pytz.utc.localize(self.fecha_agregacion).astimezone(bolivia_tz)
        
        return {
            'id': self.id,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal,
            'fecha_agregacion': fecha_agregacion_bolivia.isoformat(),
            'orden_cod': self.orden_cod,
            'producto_id': self.producto_id,
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<DetalleOrden {self.id} - Orden {self.orden_cod}>'