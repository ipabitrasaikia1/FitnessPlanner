"""Streamlit App: AI Personalized Workout Plan Generator.

Built for the Codebasics AI Engineering Cohort Assignment.
Uses Groq API with robust prompt engineering and error handling.
"""
import os
import importlib
import streamlit as st
from dotenv import load_dotenv

import planner.generator
importlib.reload(planner.generator)

from planner.models import FITNESS_GOALS, EXPERIENCE_LEVELS, EQUIPMENT_OPTIONS
from planner.generator import generate_workout_plan, get_available_models, DEFAULT_MODEL

# Load .env variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Workout Plan Generator",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished aesthetic
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #6c757d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    .stAlert {
        border-radius: 8px;
    }
    .plan-container {
        background-color: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 1.5rem;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None
if "variation_count" not in st.session_state:
    st.session_state.variation_count = 0
if "last_params" not in st.session_state:
    st.session_state.last_params = {}


# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key Handling (from environment or manual input)
    env_api_key = os.getenv("GROQ_API_KEY", "")
    api_key_input = st.text_input(
        "Groq API Key",
        value=env_api_key,
        type="password",
        help="Enter your Groq API key or set GROQ_API_KEY in your .env file.",
        placeholder="gsk_..."
    )

    if not api_key_input:
        st.info("💡 Get a free Groq API key at [console.groq.com/keys](https://console.groq.com/keys)")

    available_models = get_available_models(api_key_input)
    default_index = 0
    model_option = st.selectbox(
        "Groq Model",
        options=available_models,
        index=default_index,
        help="Select any available LLM from your Groq account.",
    )

    st.markdown("---")
    st.markdown("### 📋 Assignment Details")
    st.caption(
        "**AI Engineering Cohort** - Codebasics\n\n"
        "Features:\n"
        "- Structured Input Collection\n"
        "- Guardrailed Prompt Engineering\n"
        "- Resilient Error Handling\n"
        "- Session State Persistence\n"
        "- Download Routine (.md)"
    )


# --- MAIN CONTENT AREA ---
st.markdown('<div class="main-title">🏋️‍♂️ Personalized Workout Plan Generator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Transform your fitness goals and schedule into an actionable, professional weekly training regimen powered by Groq LLM.</div>',
    unsafe_allow_html=True,
)

# Form Section with Structured Inputs
with st.container():
    st.subheader("1. Your Fitness Profile & Constraints")
    
    col1, col2 = st.columns(2)
    with col1:
        fitness_goal = st.selectbox(
            "🎯 Primary Fitness Goal *",
            options=FITNESS_GOALS,
            index=0,
            help="What is your main target for this training phase?",
        )
        experience_level = st.selectbox(
            "🏅 Experience Level *",
            options=EXPERIENCE_LEVELS,
            index=0,
            help="Choose your experience with resistance training.",
        )

    with col2:
        days_per_week = st.slider(
            "📅 Available Days per Week *",
            min_value=1,
            max_value=7,
            value=4,
            help="How many days can you commit to exercising?",
        )
        equipment_access = st.selectbox(
            "🎒 Available Equipment *",
            options=EQUIPMENT_OPTIONS,
            index=1,
            help="The AI will strictly restrict exercise choices to what you have access to.",
        )

    limitations = st.text_input(
        "🩹 Physical Limitations or Injuries (Optional)",
        placeholder="e.g. Bad lower back, left shoulder impingement, avoid jumping / high impact",
        help="The personal trainer AI will adjust movements and add safety disclaimers for these areas.",
    )

st.write("") # spacing

# Action Buttons
btn_col1, btn_col2, _ = st.columns([1.5, 1.8, 3])

with btn_col1:
    generate_clicked = st.button("🚀 Generate Plan", type="primary", use_container_width=True)

with btn_col2:
    regenerate_clicked = st.button(
        "🔄 Regenerate Variation",
        disabled=(st.session_state.workout_plan is None),
        use_container_width=True,
        help="Generate an alternative exercise variation using the same parameters."
    )

# Logic for Generation / Regeneration
should_generate = generate_clicked or regenerate_clicked

if should_generate:
    if regenerate_clicked:
        st.session_state.variation_count += 1
    else:
        st.session_state.variation_count = 0

    with st.spinner("🤖 Coach Groq is designing your custom workout routine..."):
        success, result = generate_workout_plan(
            fitness_goal=fitness_goal,
            experience_level=experience_level,
            days_per_week=days_per_week,
            equipment_access=equipment_access,
            limitations=limitations,
            api_key=api_key_input,
            model=model_option,
            variation_seed=st.session_state.variation_count if regenerate_clicked else None,
        )

        if success:
            st.session_state.workout_plan = result
            st.session_state.last_params = {
                "goal": fitness_goal,
                "experience": experience_level,
                "days": days_per_week,
                "equipment": equipment_access,
                "limitations": limitations or "None",
            }
            st.success("✅ Workout plan successfully created!")
        else:
            # Display friendly error message without crashing
            st.error(result)

# Display Generated Workout Plan (Persists across reruns via st.session_state)
if st.session_state.workout_plan:
    st.markdown("---")
    st.subheader("📋 Your Personalized Routine")

    # Header with metadata summary and download action
    meta = st.session_state.last_params
    if meta:
        st.caption(
            f"**Goal**: {meta.get('goal')} | **Experience**: {meta.get('experience')} | "
            f"**Commitment**: {meta.get('days')} days/wk | **Equipment**: {meta.get('equipment')} | "
            f"**Limitations**: {meta.get('limitations')}"
        )

    # Markdown rendered output
    st.markdown(st.session_state.workout_plan)

    # Download Button (Stretch goal)
    st.write("")
    plan_filename = f"workout_plan_{meta.get('goal', 'routine').lower().replace(' ', '_')}.md"
    st.download_button(
        label="💾 Download Plan as Markdown (.md)",
        data=st.session_state.workout_plan,
        file_name=plan_filename,
        mime="text/markdown",
    )

