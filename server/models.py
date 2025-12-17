from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import UniqueConstraint, CheckConstraint
from datetime import date

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
    

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # ---- Table Constraint (2) ----
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_duration_positive"),
    )

    # ---- Model Validation ----
    @validates("duration_minutes")
    def validate_duration_minutes(self, _, value):
        if not isinstance(value, int):
            raise ValueError("duration_minutes must be an integer.")
        if value <= 0:
            raise ValueError("duration_minutes must be greater than 0.")
        return value
