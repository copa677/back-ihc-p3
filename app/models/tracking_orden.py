from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class TrackingOrden(db.Model):
    __tablename__ = 'tracking_orden'
    
    id = db.Column(db.Integer, primary_key=True)
    orden_cod = db.Column(db.Integer, db.ForeignKey('orden.cod'), nullable=False)
    user_delivery_id = db.Column(db.Integer, db.ForeignKey('user_delivery.id'), nullable=False)
    estado = db.Column(db.String(50), nullable=False)  # 'asignada', 'recogiendo', 'en_camino', 'entregada', 'cancelada'
    latitud = db.Column(db.Numeric(10, 7))
    longitud = db.Column(db.Numeric(10, 7))
    comentario = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=lambda: get_bolivia_time())
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: get_bolivia_time(), onupdate=lambda: get_bolivia_time())

    # Relaciones
    orden = db.relationship('Orden', backref='trackings')
    user_delivery = db.relationship('UserDelivery', backref='trackings')

    def to_dict(self):
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        fecha_creacion_bolivia = self.fecha_creacion
        fecha_actualizacion_bolivia = self.fecha_actualizacion
        
        if self.fecha_creacion.tzinfo is None:
            fecha_creacion_bolivia = pytz.utc.localize(self.fecha_creacion).astimezone(bolivia_tz)
        if self.fecha_actualizacion.tzinfo is None:
            fecha_actualizacion_bolivia = pytz.utc.localize(self.fecha_actualizacion).astimezone(bolivia_tz)
        
        return {
            'id': self.id,
            'orden_cod': self.orden_cod,
            'user_delivery_id': self.user_delivery_id,
            'estado': self.estado,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'comentario': self.comentario,
            'fecha_creacion': fecha_creacion_bolivia.isoformat(),
            'fecha_actualizacion': fecha_actualizacion_bolivia.isoformat(),
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<TrackingOrden {self.id} - Orden {self.orden_cod}>'