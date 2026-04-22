# app.py
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from models import db, Exercise, Workout, WorkoutExercise
from schemas import (exercise_schema, exercises_schema,
                     workout_schema, workouts_schema, workout_exercise_schema)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# ── WORKOUT ROUTES ───────────────────────────────────────────

@app.route('/workouts', methods=['GET'])
def get_workouts():
    # return all workouts as JSON
    return jsonify(workouts_schema.dump(Workout.query.all()))


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    # return one workout with its exercises (includes reps/sets/duration)
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout))


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        # validate request body, then save to db
        workout = Workout(**workout_schema.load(request.get_json()))
        db.session.add(workout)
        db.session.commit()
        return jsonify(workout_schema.dump(workout)), 201
    except (ValidationError, ValueError) as e:
        return jsonify({'error': e.messages if hasattr(e, 'messages') else str(e)}), 400


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    # cascade in model automatically deletes linked workout_exercises
    workout = Workout.query.get(id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted'}), 200


# ── EXERCISE ROUTES ──────────────────────────────────────────

@app.route('/exercises', methods=['GET'])
def get_exercises():
    # return all exercises as JSON
    return jsonify(exercises_schema.dump(Exercise.query.all()))


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    # return one exercise with its associated workouts
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise))


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        # validate request body, then save to db
        exercise = Exercise(**exercise_schema.load(request.get_json()))
        db.session.add(exercise)
        db.session.commit()
        return jsonify(exercise_schema.dump(exercise)), 201
    except (ValidationError, ValueError) as e:
        return jsonify({'error': e.messages if hasattr(e, 'messages') else str(e)}), 400


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    # cascade in model automatically deletes linked workout_exercises
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted'}), 200


# ── WORKOUT-EXERCISE JOIN ROUTE ──────────────────────────────

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    # make sure both the workout and exercise exist first
    if not Workout.query.get(workout_id):
        return jsonify({'error': 'Workout not found'}), 404
    if not Exercise.query.get(exercise_id):
        return jsonify({'error': 'Exercise not found'}), 404
    try:
        # validate body (reps/sets/duration), then link exercise to workout
        data = workout_exercise_schema.load(request.get_json() or {})
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(we)
        db.session.commit()
        return jsonify(workout_exercise_schema.dump(we)), 201
    except (ValidationError, ValueError) as e:
        return jsonify({'error': e.messages if hasattr(e, 'messages') else str(e)}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)