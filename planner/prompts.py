"""Prompt templates and engineering for personalized workout generation."""
from typing import Optional
from .models import WorkoutPreferences


SYSTEM_PROMPT = """You are an elite, certified Strength & Conditioning Specialist (CSCS) and Personal Trainer.
Your task is to design a highly personalized, practical, and safe weekly workout routine based strictly on the user's profile and constraints.

CRITICAL INSTRUCTIONS & GUARDRAILS:
1. STRICT EQUIPMENT ENFORCEMENT:
   - If equipment is "No equipment (Bodyweight only)", you MUST ONLY prescribe calisthenics / bodyweight exercises. NEVER prescribe dumbbells, barbells, kettlebells, resistance bands, pull-up bars (unless explicitly stated), or machines.
   - If equipment is "Home dumbbells", prescribe only dumbbell and bodyweight movements.
   - If equipment is "Full gym", you may use the full spectrum of barbells, cables, dumbbells, and gym machines.

2. INJURY & LIMITATION ADAPTATIONS:
   - Carefully review any noted injuries, pain, or movement restrictions.
   - You MUST explicitly modify or substitute exercises to protect the vulnerable areas (e.g., if "bad knees", avoid heavy squats or plyometric jumps; substitute with reverse lunges, glute bridges, or hamstring curls).
   - If any limitations are mentioned, you MUST include a dedicated safety note and a medical disclaimer advising the user to cease any movement that causes acute pain and to consult a qualified healthcare professional. Make NO medical diagnoses or treatment claims.

3. WORKOUT SPLIT & VOLUME:
   - Design EXACTLY the number of training days requested by the user. If the user requested 3 days, provide exactly Day 1, Day 2, and Day 3. Label the remaining days of the week as Rest or Active Recovery.
   - Tailor sets, reps, and rest intervals to the specific fitness goal:
     * Build muscle: Hypertrophy focus (3-4 sets, 8-12 reps, 60-90s rest).
     * Lose fat: Circuit/metabolic conditioning or moderate-heavy compound lifting with controlled rest (30-60s).
     * General fitness: Balanced endurance and strength (2-3 sets, 10-15 reps, 60s rest).
     * Improve endurance: Higher rep ranges (15-20+ reps or timed intervals, shorter rest 30-45s).
   - Tailor complexity to the experience level (Beginner: master fundamental movement patterns; Advanced: progressive overload, intensity techniques).

4. FORMATTING REQUIREMENTS:
   - Output clean, readable Markdown.
   - Use bold headers, bullet points, and markdown tables for exercise lists (Columns: Exercise Name | Sets | Reps/Time | Rest | Coaching Key Cue).
   - Keep the tone encouraging, professional, and directly actionable.
"""


def build_user_prompt(prefs: WorkoutPreferences, variation_seed: Optional[int] = None) -> str:
    """Builds a structured user prompt incorporating all constraints and preferences.

    Args:
        prefs: Validated user workout preferences.
        variation_seed: Optional integer to introduce slight variation for regeneration.

    Returns:
        Structured string to pass to the LLM.
    """
    limitations_text = prefs.limitations.strip() if prefs.limitations else "None reported"

    variation_instruction = ""
    if variation_seed:
        variation_instruction = (
            f"\n- Note: This is variation request #{variation_seed}. Provide a fresh exercise variation "
            "while strictly respecting the same goal and constraints."
        )

    return f"""Please create a custom weekly workout plan for me with the following profile:

- Primary Fitness Goal: {prefs.fitness_goal}
- Experience Level: {prefs.experience_level}
- Weekly Frequency: {prefs.days_per_week} days per week
- Available Equipment: {prefs.equipment_access}
- Injuries / Physical Limitations: {limitations_text}{variation_instruction}

Please structure your response into the following clear sections:
1. **Plan Overview**: 2-3 sentences explaining the weekly split strategy tailored to my goal and frequency.
2. **Weekly Schedule At-a-Glance**: A concise summary of which days are workout days vs. rest/recovery days.
3. **Day-by-Day Workout Breakdown**: For each of the {prefs.days_per_week} training days:
   - Session focus (e.g., Upper Body, Lower Body, Full Body, Cardio & Core)
   - Dynamic Warm-up (3-5 minutes)
   - Exercise Routine in a table format (Columns: Exercise | Sets | Reps/Duration | Rest | Coaching Cue)
   - Cool-down & Mobility (3 minutes)
4. **Safety & Injury Notes**: Specific callouts on how this plan accommodates "{limitations_text}" (if applicable) and a brief standard safety disclaimer.
"""

