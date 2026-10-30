"""Core module for generating workout plans via Groq API."""
import os
from typing import Optional, Tuple
from dotenv import load_dotenv
from groq import Groq, AuthenticationError, RateLimitError, APIConnectionError, APIStatusError, GroqError

from .models import WorkoutPreferences
from .prompts import SYSTEM_PROMPT, build_user_prompt

# Load environment variables from .env if present
load_dotenv()

DEFAULT_MODEL: str = "llama-3.3-70b-versatile"


def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
    limitations: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    variation_seed: Optional[int] = None,
) -> Tuple[bool, str]:
    """Generates a personalized, structured workout plan using Groq API.

    Args:
        fitness_goal: Primary fitness goal (e.g. "Build muscle", "Lose fat").
        experience_level: User's training experience level (e.g. "Beginner").
        days_per_week: Number of workout days available per week (1-7).
        equipment_access: Available workout equipment (e.g. "No equipment").
        limitations: Optional injuries or physical limitations.
        api_key: Optional Groq API key; if not provided, reads GROQ_API_KEY from environment.
        model: Groq model identifier (defaults to llama-3.3-70b-versatile).
        variation_seed: Optional integer to introduce slight variation for regenerated plans.

    Returns:
        Tuple[bool, str]: (Success boolean, Response markdown text or friendly error message).
    """
    # 1. Structured Input Validation
    prefs = WorkoutPreferences(
        fitness_goal=fitness_goal,
        experience_level=experience_level,
        days_per_week=days_per_week,
        equipment_access=equipment_access,
        limitations=limitations,
    )

    validation_error = prefs.validate()
    if validation_error:
        return False, f"⚠️ **Invalid Input**: {validation_error}"

    # 2. API Key Retrieval & Validation
    resolved_api_key = api_key.strip() if api_key and api_key.strip() else os.getenv("GROQ_API_KEY", "").strip()
    if not resolved_api_key:
        return (
            False,
            "🔑 **Groq API Key Required**: Please provide a valid Groq API key in the sidebar "
            "or set `GROQ_API_KEY` in your `.env` file.\n\n"
            "You can get a free API key at [console.groq.com/keys](https://console.groq.com/keys).",
        )

    # 3. Prompt Construction
    user_prompt = build_user_prompt(prefs, variation_seed=variation_seed)

    # 4. Groq API Call with granular exception handling
    try:
        client = Groq(api_key=resolved_api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.6 if variation_seed else 0.4,
            max_tokens=2500,
        )

        # 5. Response Integrity Verification
        if not response or not response.choices:
            return (
                False,
                "⚠️ **Empty Response**: The AI service returned an empty plan. "
                "Please try clicking 'Generate Plan' again.",
            )

        content: Optional[str] = response.choices[0].message.content
        if not content or not content.strip():
            return (
                False,
                "⚠️ **Malformed Response**: Received a blank response from the AI model. "
                "Please try again or select a different model variation.",
            )

        return True, content.strip()

    except AuthenticationError:
        return (
            False,
            "🚫 **Authentication Failed**: The Groq API key provided is invalid or expired. "
            "Please verify your key at [console.groq.com/keys](https://console.groq.com/keys).",
        )
    except RateLimitError:
        return (
            False,
            "⏳ **Rate Limit Exceeded**: You've hit Groq's request rate limit. "
            "Please wait a few moments and try again.",
        )
    except APIConnectionError:
        return (
            False,
            "📡 **Network Error**: Unable to reach Groq API servers. "
            "Please check your internet connection and try again.",
        )
    except APIStatusError as e:
        return (
            False,
            f"❌ **Groq Service Error** (Status {e.status_code}): {e.message}. "
            "Please try again shortly.",
        )
    except GroqError as e:
        return (
            False,
            f"❌ **Groq API Error**: {str(e)}.",
        )
    except Exception as e:
        return (
            False,
            f"⚠️ **Unexpected Error**: An unexpected issue occurred ({type(e).__name__}: {str(e)}). "
            "Please check your inputs and try again.",
        )
