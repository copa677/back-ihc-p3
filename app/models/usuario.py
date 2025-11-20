from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    tipo_usuario = db.Column(db.String(20), nullable=False, default='usuario')  # 'admin', 'usuario', etc.
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    esta_activo = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """Genera el hash de la contraseña"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña con el hash almacenado"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convierte el objeto a diccionario para JSON"""
        return {
            'id': self.id,
            'username': self.username,
            'tipo_usuario': self.tipo_usuario,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'esta_activo': self.esta_activo
        }

    def __repr__(self):
        return f'<Usuario {self.username}>'