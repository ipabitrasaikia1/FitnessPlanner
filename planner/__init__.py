"""Workout Planner Package."""
from .generator import generate_workout_plan
from .models import WorkoutPreferences

__all__ = ["generate_workout_plan", "WorkoutPreferences"]
