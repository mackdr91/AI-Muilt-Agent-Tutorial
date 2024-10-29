import streamlit as st
from ai import ask_ai, get_macros
from profiles import get_profile, create_profile, get_notes
from form_submit import update_personal_data, add_note, delete_note

st.title("Personal Fitness App")


@st.fragment()
def personal_data_form():
    with st.form("personal_data_form"):
        st.header("Personal Data")

        profile = st.session_state.profile

        name = st.text_input("Name", value=profile["general"]["name"])
        age = st.number_input(
            "Age", min_value=1, max_value=100, step=1, value=profile["general"]["age"]
        )

        genders = ["Male", "Female", "Other"]
        gender = st.radio(
            "Gender", genders, genders.index(profile["general"].get("gender", "Male"))
        )

        height = st.number_input(
            "Height (inches)",
            min_value=0,
            max_value=100,
            step=1,
            value=profile["general"]["height"],
        )
        weight = st.number_input(
            "Weight (lbs)",
            min_value=0,
            max_value=1000,
            step=1,
            value=profile["general"]["weight"],
        )
        activities = [
            "Sedentary",
            "Lightly Active",
            "Moderately Active",
            "Very Active",
            "Extremely Active",
        ]
        activity_level = st.selectbox(
            "Activity Level",
            activities,
            activities.index(profile["general"].get("activity_level", "Sedentary")),
        )
        submit_button = st.form_submit_button("Save")

        if submit_button:
            if all([name, age, gender, height, weight, activity_level]):
                with st.spinner("Calculating results..."):
                    # save data
                    st.session_state.profile = update_personal_data(
                        profile,
                        "general",
                        name=name,
                        age=age,
                        gender=gender,
                        height=height,
                        weight=weight,
                        activity_level=activity_level,
                    )

                    st.success("Data saved successfully!")
            else:
                st.warning("Please fill in all the fields.")


@st.fragment()
def goals_form():
    with st.form("goals_form"):
        st.header("Goals")

        profile = st.session_state.profile
        goals = st.multiselect(
            "Select yours goals",
            ["Muscle Gain", "Weight Loss", "Cardio"],
            default=profile.get("goals", ["Muscle Gain"]),
        )
        submit_button = st.form_submit_button("Save")

        if submit_button:
            if goals:
                with st.spinner("Calculating results..."):
                    st.session_state.profile = update_personal_data(
                        profile, "goals", goals=goals
                    )
                    st.success("Goals saved successfully!")
            else:
                st.warning("Please select at least one goal.")


@st.fragment()
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border=True)
    nutrition.header("Macros")
    if nutrition.button("Generate with AI"):
        result = get_macros(profile.get("general"), profile.get("goals"))
        profile["nutrition"] = result
        nutrition.success("Macros generated successfully!")
    with nutrition.form("nutrition_form", border=False):
        col1, col2, col3, col4 = nutrition.columns(4)
        with col1:
            calories = st.number_input(
                "Calories",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("calories", 0),
            )
        with col2:
            protein = st.number_input(
                "Protein",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("protein", 0),
            )
        with col3:
            fat = st.number_input(
                "Fat",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("fat", 0),
            )
        with col4:
            carbs = st.number_input(
                "Carbs",
                min_value=0,
                step=1,
                value=profile["nutrition"].get("carbs", 0),
            )
        submit_button = st.form_submit_button("Save")

        if submit_button:
            if all([calories, protein, fat, carbs]):
                with st.spinner("Calculating results..."):
                    st.session_state.profile = update_personal_data(
                        profile,
                        "nutrition",
                        calories=calories,
                        protein=protein,
                        fat=fat,
                        carbs=carbs,
                    )
                    st.success("Nutrition saved successfully!")
            else:
                st.warning("Please fill in all the fields.")


@st.fragment()
def notes():
    st.header("Notes: ")
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5,1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=note.get("_id")):
                delete_note(note.get("_id"))
                st.session_state.notes.pop(i)
                st.rerun()

    new_note = st.text_area("Add new note")
    if st.button("Add Note"):
        if new_note:
            note = add_note(new_note, st.session_state.profile_id)
            st.session_state.notes.append(note)
            st.rerun()

@st.fragment()
def ask_ai_func():
    st.header("Ask AI")
    user_question = st.text_area("Ask your question")
    if st.button("Ask"):
        with st.spinner("Calculating results..."):
            result = ask_ai(st.session_state.profile, user_question)
            st.write(result)

def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = get_profile(profile_id)
        if not profile:
            profile_id, profile = create_profile(profile_id)

        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = get_notes(st.session_state.profile_id)

    personal_data_form()


if __name__ == "__main__":
    forms()
    goals_form()
    macros()
    notes()
    ask_ai_func()
