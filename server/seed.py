#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    print("Deleting existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    pushups = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )

    squats = Exercise(
        name="Squats",
        category="Strength",
        equipment_needed=False
    )

    plank = Exercise(
        name="Plank",
        category="Core",
        equipment_needed=False
    )

    db.session.add_all([pushups, squats, plank])
    db.session.commit()

    print("Creating workout...")
    workout = Workout(
        date=date.today(),
        duration_minutes=30,
        notes="Morning workout"
    )

    db.session.add(workout)
    db.session.commit()

    print("Linking exercises to workout...")
    we1 = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=pushups.id,
        reps=15,
        sets=3
    )

    we2 = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=squats.id,
        reps=20,
        sets=3
    )

    we3 = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=plank.id,
        duration_seconds=60
    )

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete!")