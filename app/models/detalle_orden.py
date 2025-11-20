from app import db
from datetime import datetime

class DetalleOrden(db.Model):
    __tablename__ = 'detalle_orden'
    
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    fecha_agregacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    orden_cod = db.Column(db.Integer, db.ForeignKey('orden.cod'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)

    @property
    def subtotal(self):
        """Calcula el subtotal del detalle"""
        return self.precio_unitario * self.cantidad

    def to_dict(self):
        return {
            'id': self.id,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal,
            'fecha_agregacion': self.fecha_agregacion.isoformat() if self.fecha_agregacion else None,
            'orden_cod': self.orden_cod,
            'producto_id': self.producto_id
        }

    def __repr__(self):
        return f'<DetalleOrden {self.id} - Orden {self.orden_cod}>'