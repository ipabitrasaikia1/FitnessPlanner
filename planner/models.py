"""Data models and constants for workout planner."""
from dataclasses import dataclass
from typing import Optional, List


FITNESS_GOALS: List[str] = [
    "Build muscle",
    "Lose fat",
    "General fitness",
    "Improve endurance",
]

EXPERIENCE_LEVELS: List[str] = [
    "Beginner",
    "Intermediate",
    "Advanced",
]

EQUIPMENT_OPTIONS: List[str] = [
    "No equipment (Bodyweight only)",
    "Home dumbbells",
    "Full gym",
]


@dataclass
class WorkoutPreferences:
    """User preferences and constraints for workout routine generation."""
    fitness_goal: str
    experience_level: str
    days_per_week: int
    equipment_access: str
    limitations: Optional[str] = None

    def validate(self) -> Optional[str]:
        """Validates input fields. Returns an error message if invalid, else None."""
        if not self.fitness_goal or self.fitness_goal not in FITNESS_GOALS:
            return f"Please select a valid fitness goal from: {', '.join(FITNESS_GOALS)}."

        if not self.experience_level or self.experience_level not in EXPERIENCE_LEVELS:
            return f"Please select an experience level from: {', '.join(EXPERIENCE_LEVELS)}."

        if not isinstance(self.days_per_week, int) or self.days_per_week < 1 or self.days_per_week > 7:
            return "Days available per week must be between 1 and 7 days."

        if not self.equipment_access or self.equipment_access not in EQUIPMENT_OPTIONS:
            return f"Please select equipment access from: {', '.join(EQUIPMENT_OPTIONS)}."

        return None

