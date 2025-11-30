from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class DatosPago(db.Model):
    __tablename__ = 'datos_pago'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_tarjeta = db.Column(db.String(16), nullable=False)
    fecha_expiracion_tarjeta = db.Column(db.String(7), nullable=False)  # Formato: MM/YYYY
    nombre_propietario = db.Column(db.String(150), nullable=False)
    codigo_seguridad = db.Column(db.String(4), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    user_telegram_id = db.Column(db.Integer, db.ForeignKey('user_telegram.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: get_bolivia_time())

    def to_dict(self):
        # Convertir a zona horaria de Bolivia para la respuesta
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        fecha_creacion_bolivia = self.fecha_creacion
        
        # Si la fecha está en UTC, convertirla a Bolivia
        if self.fecha_creacion.tzinfo is None:
            fecha_creacion_bolivia = pytz.utc.localize(self.fecha_creacion).astimezone(bolivia_tz)
        
        return {
            'id': self.id,
            'numero_tarjeta': self.numero_tarjeta,
            'fecha_expiracion_tarjeta': self.fecha_expiracion_tarjeta,
            'nombre_propietario': self.nombre_propietario,
            'codigo_seguridad': self.codigo_seguridad,
            'pais': self.pais,
            'codigo_postal': self.codigo_postal,
            'user_telegram_id': self.user_telegram_id,
            'fecha_creacion': fecha_creacion_bolivia.isoformat(),
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<DatosPago {self.nombre_propietario}>'