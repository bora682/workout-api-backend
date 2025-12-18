from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates, relationship
from sqlalchemy import UniqueConstraint, CheckConstraint, ForeignKey
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

    # ---- Relationships ----
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    workouts = relationship(
        "Workout",
        secondary="workout_exercises",
        viewonly=True
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

    # ---- Relationships ----
    workout_exercises = relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    exercises = relationship(
        "Exercise",
        secondary="workout_exercises",
        viewonly=True
    )

    # ---- Model Validation ----
    @validates("duration_minutes")
    def validate_duration_minutes(self, _, value):
        if not isinstance(value, int):
            raise ValueError("duration_minutes must be an integer.")
        if value <= 0:
            raise ValueError("duration_minutes must be greater than 0.")
        return value
    

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    workout_id = db.Column(
        db.Integer,
        ForeignKey("workouts.id"),
        nullable=False
    )

    exercise_id = db.Column(
        db.Integer,
        ForeignKey("exercises.id"),
        nullable=False
    )

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # ---- Table Constraints ----
    __table_args__ = (
        UniqueConstraint(
            "workout_id",
            "exercise_id",
            name="uq_workout_exercise"
        ),
        CheckConstraint(
            "(reps IS NULL) OR (reps > 0)",
            name="ck_reps_positive"
        ),
        CheckConstraint(
            "(sets IS NULL) OR (sets > 0)",
            name="ck_sets_positive"
        ),
        CheckConstraint(
            "(duration_seconds IS NULL) OR (duration_seconds > 0)",
            name="ck_duration_seconds_positive"
        ),
        CheckConstraint(
            "(reps IS NOT NULL) OR (sets IS NOT NULL) OR (duration_seconds IS NOT NULL)",
            name="ck_at_least_one_metric"
        ),
    )

    # ---- Relationships ----
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")

    # ---- Model Validation ----
    @validates("reps", "sets", "duration_seconds")
    def validate_metrics(self, key, value):
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError(f"{key} must be an integer.")
        if value <= 0:
            raise ValueError(f"{key} must be greater than 0.")
        return value
