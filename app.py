import json
from pathlib import Path

import pandas as pd
import streamlit as st

DB = Path("school_data.json")  # same file your original script uses

st.set_page_config(page_title="School Manager", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    .stApp { background: #f7f9fc; }
    section[data-testid="stSidebar"] { background: #eef3fb; }
    div[data-testid="stMetric"] {
        background: white; padding: 18px 22px; border-radius: 14px;
        border: 1px solid #e3e9f3; box-shadow: 0 2px 8px rgba(80,110,160,.08);
    }
    .stButton > button, .stFormSubmitButton > button {
        background: #4f7cff; color: white; border: 0; border-radius: 10px; padding: .5rem 1.4rem;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover { background: #3a64e0; color: white; }
</style>
""", unsafe_allow_html=True)


# ---------- data layer ----------
def load():
    return json.loads(DB.read_text()) if DB.exists() else {"students": [], "teachers": []}


def save(d):
    DB.write_text(json.dumps(d, indent=4))


def valid_email(email):
    return "@" in email and "." in email


def average(grades):
    return sum(grades.values()) / len(grades) if grades else 0


data = load()

# ---------- navigation ----------
st.sidebar.title("🎓 School Manager")
page = st.sidebar.radio("Go to", [
                        "Dashboard", "Students", "Teachers", "Grades"], label_visibility="collapsed")


# ---------- pages ----------
def dashboard():
    st.title("Dashboard")
    students, teachers = data["students"], data["teachers"]
    avgs = [average(s["grades"]) for s in students if s["grades"]]

    c1, c2, c3 = st.columns(3)
    c1.metric("Students", len(students))
    c2.metric("Teachers", len(teachers))
    c3.metric("Class average", f"{sum(avgs) / len(avgs):.1f}" if avgs else "–")

    st.subheader("Student averages")
    if avgs:
        df = pd.DataFrame(
            {"Student": [s["name"] for s in students if s["grades"]], "Average": avgs})
        st.bar_chart(df.set_index("Student"), color="#4f7cff")
    else:
        st.info("No grades yet. Add some in the Grades page.")


def students_page():
    st.title("Students")
    tab_reg, tab_list = st.tabs(["➕ Register", "📋 Directory"])

    with tab_reg:
        with st.form("student_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Name")
            email = c2.text_input("Email")
            age = c1.number_input("Age", 3, 100, 18)
            roll_no = c2.number_input("Roll no", 1, step=1)
            if st.form_submit_button("Register student"):
                if not name.strip():
                    st.error("Name is required.")
                elif not valid_email(email):
                    st.error("Enter a valid email.")
                elif any(s["roll_no"] == roll_no for s in data["students"]):
                    st.warning("Student already exists.")
                else:
                    data["students"].append(
                        {"name": name, "age": age, "email": email,
                            "roll_no": roll_no, "grades": {}}
                    )
                    save(data)
                    st.success(f"Student {name} registered 🎉")

    with tab_list:
        if not data["students"]:
            st.info("No students registered yet.")
            return
        df = pd.DataFrame(data["students"])
        df["average"] = df["grades"].apply(average).round(1)
        st.dataframe(df.drop(columns="grades"),
                     use_container_width=True, hide_index=True)

        st.subheader("Student details")
        pick = st.selectbox(
            "Select a student", data["students"], format_func=lambda s: f"{s['roll_no']} – {s['name']}")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.metric("Average", f"{average(pick['grades']):.1f}")
            st.write(
                f"**Age:** {pick['age']}  \n**Email:** {pick['email']}  \n**Roll no:** {pick['roll_no']}")
        with c2:
            if pick["grades"]:
                st.bar_chart(
                    pd.Series(pick["grades"], name="Marks"), color="#4f7cff")
            else:
                st.caption("No grades yet.")


def teachers_page():
    st.title("Teachers")
    tab_reg, tab_list = st.tabs(["➕ Register", "📋 Directory"])

    with tab_reg:
        with st.form("teacher_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Name")
            email = c2.text_input("Email")
            age = c1.number_input("Age", 18, 100, 30)
            emp_id = c2.number_input("Employee ID", 1, step=1)
            subject = c1.text_input("Subject")
            if st.form_submit_button("Register teacher"):
                if not name.strip():
                    st.error("Name is required.")
                elif not valid_email(email):
                    st.error("Enter a valid email.")
                elif any(t["emp_id"] == emp_id for t in data["teachers"]):
                    st.warning("Teacher already exists.")
                else:
                    data["teachers"].append(
                        {"name": name, "age": age, "email": email,
                            "emp_id": emp_id, "subject": subject}
                    )
                    save(data)
                    st.success(f"Teacher {name} registered 🎉")

    with tab_list:
        if data["teachers"]:
            st.dataframe(pd.DataFrame(
                data["teachers"]), use_container_width=True, hide_index=True)
        else:
            st.info("No teachers registered yet.")


def grades_page():
    st.title("Grades")
    if not data["students"]:
        st.info("Register a student first.")
        return

    student = st.selectbox(
        "Student", data["students"], format_func=lambda s: f"{s['roll_no']} – {s['name']}")
    with st.form("grade_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        subject = c1.text_input("Subject")
        marks = c2.number_input("Marks", 0.0, 100.0, step=0.5)
        if st.form_submit_button("Save grade"):
            if subject.strip():
                student["grades"][subject.strip()] = marks
                save(data)
                st.success("Grade saved ✅")
            else:
                st.error("Subject is required.")

    if student["grades"]:
        st.subheader(f"{student['name']}'s grades")
        st.dataframe(
            pd.DataFrame(student["grades"].items(),
                         columns=["Subject", "Marks"]),
            use_container_width=True, hide_index=True,
        )
        st.metric("Average", f"{average(student['grades']):.1f}")


{"Dashboard": dashboard, "Students": students_page,
    "Teachers": teachers_page, "Grades": grades_page}[page]()
