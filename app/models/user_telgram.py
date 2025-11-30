from app import db
from datetime import datetime
import pytz

def get_bolivia_time():
    """Obtiene la hora actual en zona horaria de Bolivia (UTC-4)"""
    bolivia_tz = pytz.timezone('America/La_Paz')
    now_utc = datetime.utcnow()
    now_bolivia = now_utc.replace(tzinfo=pytz.utc).astimezone(bolivia_tz)
    return now_bolivia


class UserTelegram(db.Model):
    __tablename__ = 'user_telegram'

    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: get_bolivia_time())
    updated_at = db.Column(db.DateTime, default=lambda: get_bolivia_time(), 
                          onupdate=lambda: get_bolivia_time())

    def to_dict(self):
        # Convertir a zona horaria de Bolivia para la respuesta
        bolivia_tz = pytz.timezone('America/La_Paz')
        
        created_at_bolivia = self.created_at
        updated_at_bolivia = self.updated_at
        
        # Si las fechas están en UTC, convertirlas a Bolivia
        if self.created_at.tzinfo is None:
            created_at_bolivia = pytz.utc.localize(self.created_at).astimezone(bolivia_tz)
        if self.updated_at.tzinfo is None:
            updated_at_bolivia = pytz.utc.localize(self.updated_at).astimezone(bolivia_tz)
        
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'created_at': created_at_bolivia.isoformat(),
            'updated_at': updated_at_bolivia.isoformat(),
            'timezone': 'America/La_Paz'
        }

    def __repr__(self):
        return f'<UserTelegram {self.chat_id}>'