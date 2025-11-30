from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class Orden(db.Model):
    __tablename__ = 'orden'
    
    cod = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False, default=0.0)
    estado = db.Column(db.String(50), nullable=False, default='pendiente')  # pendiente, completada, cancelada
    fecha_creacion = db.Column(db.DateTime, default=lambda: get_bolivia_time())
    user_telegram_id = db.Column(db.Integer, db.ForeignKey('user_telegram.id'), nullable=False)

    # Relación con detalles de orden
    detalles = db.relationship('DetalleOrden', backref='orden', lazy=True, cascade='all, delete-orphan')
    # Relación con factura (una orden puede tener una factura)
    factura = db.relationship('Factura', backref='orden', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        # Convertir a zona horaria de Bolivia para la respuesta
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        fecha_creacion_bolivia = self.fecha_creacion
        
        # Si la fecha está en UTC, convertirla a Bolivia
        if self.fecha_creacion.tzinfo is None:
            fecha_creacion_bolivia = pytz.utc.localize(self.fecha_creacion).astimezone(bolivia_tz)
        
        return {
            'cod': self.cod,
            'total': self.total,
            'estado': self.estado,
            'fecha_creacion': fecha_creacion_bolivia.isoformat(),
            'user_telegram_id': self.user_telegram_id,
            'detalles_count': len(self.detalles),
            'tiene_factura': self.factura is not None,
            'timezone': 'America/La_Paz'
        }

    def calcular_total(self):
        """Calcula el total de la orden sumando todos los detalles"""
        self.total = sum(detalle.subtotal for detalle in self.detalles)
        return self.total

    def __repr__(self):
        return f'<Orden {self.cod} - {self.estado}>'