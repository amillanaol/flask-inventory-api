from datetime import datetime
from app.extensions import db


class Movement(db.Model):
    __tablename__ = "movements"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movement_type = db.Column(db.String(10), nullable=False)  # 'entry' or 'exit'
    quantity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product.name if self.product else None,
            "product_sku": self.product.sku if self.product else None,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "movement_type": self.movement_type,
            "quantity": self.quantity,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Movement {self.id} - {self.movement_type}>"
