from app import db
from datetime import datetime

class DatosEnvio(db.Model):
    __tablename__ = 'datos_envio'
    
    id = db.Column(db.Integer, primary_key=True)
    direccion1 = db.Column(db.String(200), nullable=False)
    direccion2 = db.Column(db.String(200))
    ciudad = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    nombre_completo = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    comentario = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'direccion1': self.direccion1,
            'direccion2': self.direccion2,
            'ciudad': self.ciudad,
            'region': self.region,
            'codigo_postal': self.codigo_postal,
            'nombre_completo': self.nombre_completo,
            'telefono': self.telefono,
            'comentario': self.comentario,
            'usuario_id': self.usuario_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __repr__(self):
        return f'<DatosEnvio {self.nombre_completo}>'