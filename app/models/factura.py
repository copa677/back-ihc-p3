from app import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = 'factura'
    
    cod = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False, default=0.0)
    estado = db.Column(db.String(50), nullable=False, default='pendiente')  # pendiente, pagada, cancelada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    tipo_pago = db.Column(db.String(50), nullable=False)  # tarjeta, efectivo, transferencia
    orden_cod = db.Column(db.Integer, db.ForeignKey('orden.cod'), nullable=False, unique=True)

    def to_dict(self):
        return {
            'cod': self.cod,
            'total': self.total,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'tipo_pago': self.tipo_pago,
            'orden_cod': self.orden_cod
        }

    def __repr__(self):
        return f'<Factura {self.cod} - Orden {self.orden_cod}>'