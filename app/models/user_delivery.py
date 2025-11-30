from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    return datetime.now(bolivia_tz)

class UserDelivery(db.Model):
    __tablename__ = 'user_delivery'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=lambda: get_bolivia_time())
    esta_activo = db.Column(db.Boolean, default=True)
    latitud = db.Column(db.Numeric(10,7))
    longitud = db.Column(db.Numeric(10,7))

    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña con el hash almacenado"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        # Convertir a zona horaria de Bolivia para la respuesta
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        fecha_creacion_bolivia = self.fecha_creacion
        
        # Si la fecha está en UTC, convertirla a Bolivia
        if self.fecha_creacion.tzinfo is None:
            fecha_creacion_bolivia = pytz.utc.localize(self.fecha_creacion).astimezone(bolivia_tz)
        
        return {
            'id': self.id,
            'username': self.username,
            'fecha_creacion': fecha_creacion_bolivia.isoformat(),
            'esta_activo': self.esta_activo,
            'latitud': float(self.latitud) if self.latitud else None,
            'longitud': float(self.longitud) if self.longitud else None,
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<Usuario {self.username}>'