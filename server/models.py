from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # ---- Table Constraint (1) ----
    __table_args__ = (
        UniqueConstraint("name", name="uq_exercise_name"),
    )

    # ---- Model Validations (2) ----
    @validates("name")
    def validate_name(self, _, value):
        if not value or not value.strip():
            raise ValueError("Exercise name is required.")
        if len(value.strip()) < 2:
            raise ValueError("Exercise name must be at least 2 characters.")
        return value.strip()

    @validates("category")
    def validate_category(self, _, value):
        if not value or not value.strip():
            raise ValueError("Category is required.")
        return value.strip()
