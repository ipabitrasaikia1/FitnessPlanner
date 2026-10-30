# 🏋️‍♂️ AI Personalized Workout Plan Generator

An intelligent, interactive Streamlit application that collects structured user fitness preferences and leverages the **Groq API** (powered by `llama-3.3-70b-versatile`) to generate safe, personalized, and highly usable weekly workout plans.

Built for the **Codebasics AI Engineering Cohort - Assignment 1**.

---

## 🎯 Overview & Learning Goals

This project emphasizes **thoughtful prompt engineering, strict constraint adherence, and resilient error handling**, rather than just naive API wrapping.

- **Strict Constraint Enforcement**: Guarantees zero hallucinated gym equipment when "No equipment" or "Home dumbbells" is selected.
- **Injury & Limitation Guardrails**: Automatically adapts exercises (e.g., substituting high-impact knee exercises for joint issues) and injects health/safety disclaimers.
- **Structured Outputs**: Formats routines into clean, day-by-day markdown tables with exercises, sets, reps, and rest intervals.
- **Fault-Tolerant Architecture**: Gracefully handles missing inputs, invalid API keys, rate limits, network outages, and malformed responses without crashing.

---

## 🌟 Features

| Feature | Description |
| :--- | :--- |
| **Structured Inputs** | Dropdowns for Fitness Goal and Experience Level; Slider for Weekly Days (1–7); Dropdown for Equipment; Free text for optional Limitations / Injuries. |
| **Type-Hinted Python Core** | Clean separation of UI (`app.py`) and business logic (`planner/generator.py`) using Python 3.10+ type annotations and dataclasses. |
| **Session State Persistence** | Generated plans persist across page reloads and parameter adjustments via `st.session_state`. |
| **Regenerate Variation** | Generate an alternative routine while respecting the same profile constraints. |
| **Export Routine** | One-click download of the complete workout plan as a `.md` markdown file. |
| **Sidebar Configuration** | Interactive Groq API key configuration and model selection (`llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, etc.). |

---

## 🏗️ Project Structure

```
FitnessPlanner/
├── planner/
│   ├── __init__.py         # Package exports
│   ├── models.py           # Dataclasses, validation logic & option constants
│   ├── prompts.py          # System prompt & user prompt builder with guardrails
│   └── generator.py        # Groq API caller with type hints & try/except error handling
├── tests/
│   └── test_generator.py   # Unit tests for input validation and error handling
├── .env.example            # Environment variable template
├── .gitignore              # Ignores .venv, .env, __pycache__, etc.
├── requirements.txt        # streamlit, groq, python-dotenv
├── app.py                  # Streamlit frontend user interface
└── README.md               # Documentation and setup guide
```

---

## 🚀 Quickstart Guide

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/FitnessPlanner.git
cd FitnessPlanner
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your Groq API Key
You can either:
- **Option A**: Copy `.env.example` to `.env` and insert your key:
  ```bash
  cp .env.example .env
  # Edit .env and set: GROQ_API_KEY=gsk_...
  ```
  *(Free keys available at [console.groq.com/keys](https://console.groq.com/keys))*
- **Option B**: Enter your Groq API key directly into the sidebar field inside the Streamlit app.

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Tests

Run the unit tests to verify input validation and error rejection:

```bash
python3 -m unittest discover tests/
```

---

## 📊 Rubric Compliance

| Rubric Criteria | Weight | Implementation Details |
| :--- | :--- | :--- |
| **App runs without crashing** | 20% | `WorkoutPreferences.validate()` catches boundary inputs (e.g. 0 days); friendly UI warnings shown without raising unhandled exceptions. |
| **Structured Inputs** | 25% | Multi-field input widgets mapped into type-safe dataclasses before passing into prompt templates. |
| **Prompt Design** | 30% | Clear system persona, explicit forbidden equipment rules, injury adaptation rules, structured table output format, and health disclaimers. |
| **Error Handling** | 15% | Catches `AuthenticationError`, `RateLimitError`, `APIConnectionError`, `APIStatusError`, and malformed/empty response cases. |
| **Code Quality** | 10% | Strict type hints, modular package architecture, PEP-8 compliance, and comprehensive unit tests. |
| **Stretch Goals** | Bonus | `st.session_state` persistence, "Regenerate Variation" button, and `.md` file download. |
