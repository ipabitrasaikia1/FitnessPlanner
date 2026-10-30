"""Unit tests verifying error handling, input validation, and rubric criteria."""
import unittest
from planner.models import WorkoutPreferences
from planner.generator import generate_workout_plan


class TestWorkoutPlanner(unittest.TestCase):
    def test_input_validation_invalid_days(self):
        """Verify that invalid days (0 or >7) do not crash and return friendly messages."""
        pref_zero = WorkoutPreferences(
            fitness_goal="Build muscle",
            experience_level="Beginner",
            days_per_week=0,
            equipment_access="Full gym",
        )
        err = pref_zero.validate()
        self.assertIsNotNone(err)
        self.assertIn("between 1 and 7", err)

        pref_eight = WorkoutPreferences(
            fitness_goal="Build muscle",
            experience_level="Beginner",
            days_per_week=8,
            equipment_access="Full gym",
        )
        self.assertIsNotNone(pref_eight.validate())

    def test_input_validation_invalid_goal(self):
        """Verify invalid fitness goal is caught gracefully."""
        pref = WorkoutPreferences(
            fitness_goal="Become a superhero overnight",
            experience_level="Beginner",
            days_per_week=4,
            equipment_access="Full gym",
        )
        err = pref.validate()
        self.assertIsNotNone(err)
        self.assertIn("valid fitness goal", err)

    def test_generator_missing_api_key(self):
        """Verify that calling generator without API key fails gracefully with friendly message."""
        success, message = generate_workout_plan(
            fitness_goal="Build muscle",
            experience_level="Beginner",
            days_per_week=4,
            equipment_access="Full gym",
            api_key="",  # Empty API key
        )
        self.assertFalse(success)
        self.assertIn("Groq API Key Required", message)

    def test_generator_invalid_input_rejection(self):
        """Verify that generator rejects invalid inputs before even attempting API call."""
        success, message = generate_workout_plan(
            fitness_goal="Invalid Goal",
            experience_level="Beginner",
            days_per_week=0,
            equipment_access="Full gym",
            api_key="dummy_key",
        )
        self.assertFalse(success)
        self.assertIn("Invalid Input", message)


if __name__ == "__main__":
    unittest.main()
