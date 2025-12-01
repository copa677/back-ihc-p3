from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class DatosEnvio(db.Model):
    __tablename__ = 'datos_envio'
    
    id = db.Column(db.Integer, primary_key=True)
    latitud = db.Column(db.Numeric(10,7), nullable=False)
    longitud = db.Column(db.Numeric(10,7), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    comentario = db.Column(db.Text)
    user_telegram_id = db.Column(db.Integer, db.ForeignKey('user_telegram.id'), nullable=False)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden.cod'), nullable=False)
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
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'ciudad': self.ciudad,
            'region': self.region,
            'codigo_postal': self.codigo_postal,
            'nombre_completo': self.nombre_completo,
            'telefono': self.telefono,
            'comentario': self.comentario,
            'user_telegram_id': self.user_telegram_id,
            'orden_id': self.orden_id,
            'fecha_creacion': fecha_creacion_bolivia.isoformat(),
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<DatosEnvio {self.nombre_completo}>'