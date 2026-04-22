# seed.py - resets and fills the database with sample data
from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date

with app.app_context():

    # clear all tables (order matters due to foreign keys)
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # create exercises
    e1 = Exercise(name="Push-up", category="strength",    equipment_needed=False)
    e2 = Exercise(name="Squat",   category="strength",    equipment_needed=False)
    e3 = Exercise(name="Running", category="cardio",      equipment_needed=False)
    e4 = Exercise(name="Yoga",    category="flexibility", equipment_needed=False)
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    # create workouts
    w1 = Workout(date=date(2024, 1, 10), duration_minutes=45, notes="Morning session")
    w2 = Workout(date=date(2024, 1, 12), duration_minutes=30, notes="Quick cardio")
    db.session.add_all([w1, w2])
    db.session.commit()

    # link exercises to workouts
    db.session.add_all([
        WorkoutExercise(workout_id=w1.id, exercise_id=e1.id, sets=3, reps=15),
        WorkoutExercise(workout_id=w1.id, exercise_id=e2.id, sets=4, reps=12),
        WorkoutExercise(workout_id=w2.id, exercise_id=e3.id, duration_seconds=1200),
    ])
    db.session.commit()

    print("Database seeded!")