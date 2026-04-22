# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String, nullable=False, unique=True)  # constraint: unique & required
    category         = db.Column(db.String, nullable=False)               # constraint: required
    equipment_needed = db.Column(db.Boolean, default=False)

    # one exercise -> many workout_exercises (cascade deletes them when exercise is deleted)
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts          = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, value):
        # model validation: name must not be empty
        if not value or not value.strip():
            raise ValueError("Name cannot be blank.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        # model validation: only these 4 categories are allowed
        if value not in ['strength', 'cardio', 'flexibility', 'balance']:
            raise ValueError("Category must be: strength, cardio, flexibility, or balance.")
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'

    id               = db.Column(db.Integer, primary_key=True)
    date             = db.Column(db.Date,    nullable=False)   # constraint: required
    duration_minutes = db.Column(db.Integer, nullable=False)   # constraint: required
    notes            = db.Column(db.Text)

    # one workout -> many workout_exercises (cascade deletes them when workout is deleted)
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises         = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        # model validation: duration must be a positive number
        if not value or value <= 0:
            raise ValueError("Duration must be greater than 0.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id               = db.Column(db.Integer, primary_key=True)
    workout_id       = db.Column(db.Integer, db.ForeignKey('workouts.id'),  nullable=False)
    exercise_id      = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets             = db.Column(db.Integer)
    reps             = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # each row belongs to one workout and one exercise
    workout  = db.relationship('Workout',  back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('sets')
    def validate_sets(self, key, value):
        # model validation: sets must be positive if given
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0.")
        return value