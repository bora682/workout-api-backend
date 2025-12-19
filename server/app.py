from flask import Flask, request, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()

# Routes will go here later
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(exercises_schema.dump(exercises), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    try:
        data = exercise_schema.load(request.json)
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
        return make_response(exercise_schema.dump(exercise), 201)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)


@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout_by_id(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    
    return make_response(workout_schema.dump(workout), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    try:
        data = workout_schema.load(request.json)
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
        return make_response(workout_schema.dump(workout), 201)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    
    db.session.delete(workout)
    db.session.commit()
    return make_response({}, 204)


@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    if not workout:
        return make_response({"error": "Workout not found"}, 404)
    
    exercise = Exercise.query.get(exercise_id)
    if not exercise:
        return make_response({"error": "Exercise not found"}, 404)
    
    body = request.get_json() or {}
    body["workout_id"] = workout_id
    body["exercise_id"] = exercise_id

    try:
        data = workout_exercise_schema.load(body)
        we = WorkoutExercise(**data)
        db.session.add(we)
        db.session.commit()
        return make_response(workout_exercise_schema.dump(we), 201)
    except ValidationError as e:
        return make_response({"errors": e.messages}, 400)
    except Exception as e:
        db.session.rollback()
        return make_response({"error": str(e)}, 400)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
