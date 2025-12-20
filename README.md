# Workout API Backend

## Description
A Flask REST API backend for tracking workouts and reusable exercises.
Supports CRUD operations for workouts and exercises, and adding exercises to workouts via a join table with reps, sets, or duration metrics.
Built with Flask, SQLAlchemy, Marshmallow, and SQLite, with model, table, and schema validations.

---

## Installation

```bash
git clone https://github.com/bora682/workout-api-backend.git
cd workout-api-backend
pipenv install
pipenv shell
```


## Database Setup (Migrations)

```
cd server
export FLASK_APP=app.py
flask db upgrade head
```


## Seed the Database

```
cd server
python seed.py
```


## Run the Server

```
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
flask run
```
Server runs at:
http://127.0.0.1:5555


## API Endpoints

### Exercises
- **GET** `/exercises`
Returns all exercises.
- **GET** `/exercises/<id>`
Returns a single exercise by ID.
- **POST** `/exercises`
Creates a new exercise.

Example:
```json
{
    "name": "Burpees",
    "category": "Cardio",
    "equipment_needed": false
}
```
- **DELETE** `/exercises/<id>`
Deletes an exercise by ID.

## Workouts
- **GET** `/workouts`
Returns all workouts with associated exercises.
- **GET** `/workouts/<id>`
Returns a single workout with its exercises.
- **POST** `/workouts`
Creates a new workout.

Example:
```json
{
    "date": "2025-12-19",
    "duration_minutes": 45,
    "notes": "Evening workout"
}
```
- **DELETE** `/workouts/<id>`
Deletes a workout by ID.

## WorkoutExercises (Join Table)
- **POST** `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises`
Adds an exercise to a workout with metrics.

Example:
```json
{
    "reps": 10, 
    "sets": 3
}
```
or
```json
{
    "duration_seconds": 60
}
```

## Technologies Used
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite