from app import db
from datetime import datetime

class DatosPago(db.Model):
    __tablename__ = 'datos_pago'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_tarjeta = db.Column(db.String(16), nullable=False)
    fecha_expiracion_tarjeta = db.Column(db.String(7), nullable=False)  # Formato: MM/YYYY
    nombre_propietario = db.Column(db.String(150), nullable=False)
    codigo_seguridad = db.Column(db.String(4), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'numero_tarjeta': self.numero_tarjeta,
            'fecha_expiracion_tarjeta': self.fecha_expiracion_tarjeta,
            'nombre_propietario': self.nombre_propietario,
            'codigo_seguridad': self.codigo_seguridad,
            'pais': self.pais,
            'codigo_postal': self.codigo_postal,
            'usuario_id': self.usuario_id,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None
        }

    def __repr__(self):
        return f'<DatosPago {self.nombre_propietario}>'