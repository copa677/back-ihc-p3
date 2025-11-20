from app import db
from datetime import datetime

class ItemCarrito(db.Model):
    __tablename__ = 'item_carrito'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    fecha_agregacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    carrito_id = db.Column(db.Integer, db.ForeignKey('carrito.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)

    @property
    def subtotal(self):
        """Calcula el subtotal del item"""
        return self.precio_unitario * self.cantidad

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'precio_unitario': self.precio_unitario,
            'cantidad': self.cantidad,
            'subtotal': self.subtotal,
            'fecha_agregacion': self.fecha_agregacion.isoformat() if self.fecha_agregacion else None,
            'carrito_id': self.carrito_id,
            'producto_id': self.producto_id
        }

    def __repr__(self):
        return f'<ItemCarrito {self.name} x{self.cantidad}>'