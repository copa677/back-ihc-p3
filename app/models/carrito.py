from app import db
from datetime import datetime

class Carrito(db.Model):
    __tablename__ = 'carrito'
    
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, default=0.0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relación con items del carrito
    items = db.relationship('ItemCarrito', backref='carrito', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'total': self.total,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'usuario_id': self.usuario_id,
            'esta_activo': self.esta_activo,
            'items_count': len(self.items)
        }

    def calcular_total(self):
        """Calcula el total del carrito sumando todos los items"""
        self.total = sum(item.subtotal for item in self.items)
        return self.total

    def __repr__(self):
        return f'<Carrito {self.id} - Usuario {self.usuario_id}>'