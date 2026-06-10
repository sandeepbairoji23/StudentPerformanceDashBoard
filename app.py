import streamlit as st
import pandas as pd

# Page Title
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")

# Load Data
try:
    students = pd.read_csv("Student_database.csv")
except:
    st.error("Student_database.csv file not found!")
    st.stop()

# Calculate Total and Average
students["Total"] = (
    students["Math"] +
    students["Science"] +
    students["English"]
)

students["Average"] = students["Total"] / 3

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Select Option",
    [
        "Display Students",
        "Search Student",
        "Top Performer",
        "Subject Statistics",
        "Attendance Statistics",
        "Add Student"
    ]
)

# Display Students
if menu == "Display Students":
    st.subheader("All Students")
    st.dataframe(students)

    st.metric("Total Students", len(students))

# Search Student
elif menu == "Search Student":
    st.subheader("Search Student")

    sid = st.number_input("Enter Student ID", step=1)

    if st.button("Search"):
        result = students[students["Student_ID"] == sid]

        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("Student Not Found")

# Top Performer
elif menu == "Top Performer":
    st.subheader("Top Performer")

    top = students.loc[students["Total"].idxmax()]

    st.success(f"Name: {top['Name']}")
    st.write(f"Total Marks: {top['Total']}")
    st.write(f"Average: {top['Average']:.2f}")

# Subject Statistics
elif menu == "Subject Statistics":
    st.subheader("Subject Wise Averages")

    math_avg = students["Math"].mean()
    science_avg = students["Science"].mean()
    english_avg = students["English"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric("Math", round(math_avg, 2))
    col2.metric("Science", round(science_avg, 2))
    col3.metric("English", round(english_avg, 2))

    st.bar_chart(
        pd.DataFrame({
            "Average": [math_avg, science_avg, english_avg]
        },
        index=["Math", "Science", "English"])
    )

# Attendance Statistics
elif menu == "Attendance Statistics":
    st.subheader("Attendance Statistics")

    st.metric(
        "Average Attendance",
        round(students["Attendance"].mean(), 2)
    )

    st.metric(
        "Highest Attendance",
        students["Attendance"].max()
    )

    st.bar_chart(students.set_index("Name")["Attendance"])

# Add Student
elif menu == "Add Student":
    st.subheader("Add New Student")

    sid = st.number_input("Student ID", step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", step=1)
    gender = st.selectbox("Gender", ["Male", "Female"])
    math = st.number_input("Math Marks", 0, 100)
    science = st.number_input("Science Marks", 0, 100)
    english = st.number_input("English Marks", 0, 100)
    attendance = st.number_input("Attendance", 0, 100)

    if st.button("Add Student"):

        new_student = pd.DataFrame([{
            "Student_ID": sid,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Math": math,
            "Science": science,
            "English": english,
            "Attendance": attendance
        }])

        students = pd.concat(
            [students, new_student],
            ignore_index=True
        )

        students.to_csv(
            "Student_database.csv",
            index=False
        )

        st.success("Student Added Successfully!")

# Footer
st.markdown("---")
st.write("Student Performance Management System")