from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    user_delivery_id = db.Column(db.Integer, db.ForeignKey('user_delivery.id'), nullable=False)
    orden_cod = db.Column(db.Integer, db.ForeignKey('orden.cod'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'nueva_orden', 'orden_aceptada', 'orden_rechazada'
    mensaje = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # 'pendiente', 'aceptada', 'rechazada', 'vista'
    visto = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: get_bolivia_time())
    fecha_actualizacion = db.Column(db.DateTime, default=lambda: get_bolivia_time(), onupdate=lambda: get_bolivia_time())

    # Relaciones
    user_delivery = db.relationship('UserDelivery', backref='notificaciones')
    orden = db.relationship('Orden', backref='notificaciones')

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
            'user_delivery_id': self.user_delivery_id,
            'orden_cod': self.orden_cod,
            'tipo': self.tipo,
            'mensaje': self.mensaje,
            'estado': self.estado,
            'visto': self.visto,
            'fecha_creacion': fecha_creacion_bolivia.isoformat(),
            'fecha_actualizacion': fecha_actualizacion_bolivia.isoformat(),
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<Notificacion {self.id} - {self.tipo}>'