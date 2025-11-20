from app import db
from datetime import datetime

class Orden(db.Model):
    __tablename__ = 'orden'
    
    cod = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False, default=0.0)
    estado = db.Column(db.String(50), nullable=False, default='pendiente')  # pendiente, completada, cancelada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relación con detalles de orden
    detalles = db.relationship('DetalleOrden', backref='orden', lazy=True, cascade='all, delete-orphan')
    # Relación con factura (una orden puede tener una factura)
    factura = db.relationship('Factura', backref='orden', uselist=False, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'cod': self.cod,
            'total': self.total,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_id': self.usuario_id,
            'detalles_count': len(self.detalles),
            'tiene_factura': self.factura is not None
        }

    def calcular_total(self):
        """Calcula el total de la orden sumando todos los detalles"""
        self.total = sum(detalle.subtotal for detalle in self.detalles)
        return self.total

    def __repr__(self):
        return f'<Orden {self.cod} - {self.estado}>'