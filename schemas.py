# schemas.py
from marshmallow import Schema, fields, validate


class WorkoutExerciseSchema(Schema):
    id               = fields.Int(dump_only=True)
    workout_id       = fields.Int(dump_only=True)
    exercise_id      = fields.Int(dump_only=True)
    sets             = fields.Int(load_default=None, validate=validate.Range(min=1, error="Sets must be at least 1."))   # schema validation
    reps             = fields.Int(load_default=None, validate=validate.Range(min=1, error="Reps must be at least 1."))   # schema validation
    duration_seconds = fields.Int(load_default=None)
    # when inside a workout response, show basic exercise info
    exercise = fields.Nested(lambda: ExerciseSchema(only=('id', 'name', 'category')), dump_only=True)


class ExerciseSchema(Schema):
    id               = fields.Int(dump_only=True)
    name             = fields.Str(required=True, validate=validate.Length(min=1, error="Name cannot be blank."))  # schema validation
    category         = fields.Str(required=True, validate=validate.OneOf(                                         # schema validation
        ['strength', 'cardio', 'flexibility', 'balance'],
        error="Category must be: strength, cardio, flexibility, or balance."
    ))
    equipment_needed  = fields.Bool(load_default=False)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema(exclude=('exercise',))), dump_only=True)


class WorkoutSchema(Schema):
    id               = fields.Int(dump_only=True)
    date             = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration must be at least 1."))  # schema validation
    notes            = fields.Str(load_default=None)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)


# these instances are imported and used in app.py
exercise_schema        = ExerciseSchema()
exercises_schema       = ExerciseSchema(many=True)
workout_schema         = WorkoutSchema()
workouts_schema        = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()