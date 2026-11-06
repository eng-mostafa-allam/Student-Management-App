import streamlit as st

st.set_page_config(page_title="Student Management System", layout="wide")

# keep data in session state so it doesn't reset on rerun
if "data" not in st.session_state:
    st.session_state.data = {}

data = st.session_state.data

st.title("Student Management System")

# sidebar navigation instead of the CLI while loop
menu = [
    "Add a New Student",
    "View All Students",
    "Search for a Student",
    "Update Student Grades",
    "Calculate Student Average",
    "Show the Top Student",
    "Delete a Student",
    "Show Statistics",
    "Show Passing Students",
    "Mark Attendance",
]

choice = st.sidebar.radio("Navigation", menu)

if choice == "Add a New Student":
    st.subheader("Add a New Student")

    name = st.text_input("Enter your name:").strip()
    student_id = st.number_input("Enter your ID:", min_value=1, step=1)
    age = st.number_input("Enter student age:", min_value=1, step=1)

    st.write("#### Enter Grades")
    col1, col2, col3 = st.columns(3)
    with col1:
        g1 = st.number_input(
            "Subject 1:", min_value=0.0, max_value=100.0, step=0.5
        )
    with col2:
        g2 = st.number_input(
            "Subject 2:", min_value=0.0, max_value=100.0, step=0.5
        )
    with col3:
        g3 = st.number_input(
            "Subject 3:", min_value=0.0, max_value=100.0, step=0.5
        )

    if st.button("Add Student"):
        if not name:
            st.error("Name cannot be empty. Please try again.")
        elif student_id in data:
            st.error("ID already exists. Please enter a unique ID.")
        else:
            data[student_id] = {
                "name": name,
                "age": age,
                "grades": [g1, g2, g3],
                "attendance": 0,
            }
            st.success(
                f"Student {name} with ID {student_id} added successfully."
            )

elif choice == "View All Students":
    st.subheader("All Students")
    if not data:
        st.info("No students found.")
    else:
        # sort alphabetically by name
        sorted_students = sorted(
            data.items(), key=lambda x: x[1]["name"].lower()
        )

        table_data = []
        for idx, (s_id, info) in enumerate(sorted_students, 1):
            table_data.append({
                "#": idx,
                "ID": s_id,
                "Name": info["name"],
                "Age": info["age"],
                "Grades": str(info["grades"]),
                "Attendance (days)": info["attendance"],
            })
        st.table(table_data)

elif choice == "Search for a Student":
    st.subheader("Search Student")
    if not data:
        st.info("No students found.")
    else:
        method = st.radio("Search by:", ["ID", "Name"], horizontal=True)

        if method == "ID":
            search_id = st.number_input(
                "Enter student ID:", min_value=1, step=1
            )
            if st.button("Search"):
                if search_id in data:
                    info = data[search_id]
                    st.success(
                        f"Student found: ID: {search_id}, Name: {info['name']}, Age: {info['age']}, Grades: {info['grades']}, Attendance: {info['attendance']} days"
                    )
                else:
                    st.warning("Student not found.")
        else:
            search_name = st.text_input("Enter student name:").strip().lower()
            if st.button("Search"):
                found = False
                for s_id, info in data.items():
                    if search_name == info["name"].lower():
                        st.success(
                            f"Student found: ID: {s_id}, Name: {info['name']}, Age: {info['age']}, Grades: {info['grades']}, Attendance: {info['attendance']} days"
                        )
                        found = True
                if not found:
                    st.warning("Student not found.")

elif choice == "Update Student Grades":
    st.subheader("Update Grades")
    if not data:
        st.info("No students found.")
    else:
        s_id = st.number_input(
            "Enter student ID to update:", min_value=1, step=1
        )

        if s_id in data:
            st.write(f"Updating grades for: **{data[s_id]['name']}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                new_g1 = st.number_input(
                    "New Grade 1:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(data[s_id]["grades"][0]),
                )
            with col2:
                new_g2 = st.number_input(
                    "New Grade 2:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(data[s_id]["grades"][1]),
                )
            with col3:
                new_g3 = st.number_input(
                    "New Grade 3:",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(data[s_id]["grades"][2]),
                )

            if st.button("Update Grades"):
                data[s_id]["grades"] = [new_g1, new_g2, new_g3]
                st.success(f"Grades for student ID {s_id} updated.")
        else:
            st.warning("Enter a valid existing ID to load grades.")

elif choice == "Calculate Student Average":
    st.subheader("Calculate Average")
    if not data:
        st.info("No students found.")
    else:
        s_id = st.number_input("Enter student ID:", min_value=1, step=1)
        if st.button("Calculate"):
            if s_id in data:
                grades = data[s_id]["grades"]
                avg = sum(grades) / len(grades)

                if avg >= 90:
                    res = "Excellent"
                elif avg >= 80:
                    res = "Very Good"
                elif avg >= 70:
                    res = "Good"
                elif avg >= 50:
                    res = "Pass"
                else:
                    res = "Fail"

                st.info(
                    f"Average grade for ID {s_id} ({data[s_id]['name']}): **{avg:.2f}** ({res})"
                )
            else:
                st.error("Student not found.")

elif choice == "Show the Top Student":
    st.subheader("Top Student")
    if not data:
        st.info("No students found.")
    else:
        top_id = None
        highest_avg = -1

        for s_id, info in data.items():
            avg = sum(info["grades"]) / len(info["grades"])
            if avg > highest_avg:
                highest_avg = avg
                top_id = s_id

        top_info = data[top_id]
        st.success(
            f"Top Student -> ID: {top_id} | Name: {top_info['name']} | Age: {top_info['age']} | Average: {highest_avg:.2f}"
        )

elif choice == "Delete a Student":
    st.subheader("Delete Student")
    if not data:
        st.info("No students found.")
    else:
        s_id = st.number_input(
            "Enter student ID to delete:", min_value=1, step=1
        )
        if st.button("Delete"):
            if s_id in data:
                del data[s_id]
                st.success(f"Student with ID {s_id} deleted.")
            else:
                st.error("Student not found.")

elif choice == "Show Statistics":
    st.subheader("Class Statistics")
    if not data:
        st.info("No students found.")
    else:
        averages = []
        passing = 0
        failing = 0

        for student in data.values():
            avg = sum(student["grades"]) / len(student["grades"])
            averages.append(avg)
            if avg >= 50:
                passing += 1
            else:
                failing += 1

        total = len(data)
        pass_perc = (passing / total) * 100

        # display metrics in columns
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Students", total)
        c2.metric("Class Average", f"{sum(averages)/total:.2f}")
        c3.metric("Passing Percentage", f"{pass_perc:.2f}%")

        c4, c5, c6 = st.columns(3)
        c4.metric("Highest Average", f"{max(averages):.2f}")
        c5.metric("Lowest Average", f"{min(averages):.2f}")
        c6.metric("Pass / Fail", f"{passing} / {failing}")

elif choice == "Show Passing Students":
    st.subheader("Passing Students")
    if not data:
        st.info("No students found.")
    else:
        passing_list = []
        for s_id, info in data.items():
            avg = sum(info["grades"]) / len(info["grades"])
            if avg >= 50:
                passing_list.append(
                    {"ID": s_id, "Name": info["name"], "Average": f"{avg:.2f}"}
                )

        if not passing_list:
            st.warning("No passing students found.")
        else:
            st.table(passing_list)

elif choice == "Mark Attendance":
    st.subheader("Mark Attendance")
    if not data:
        st.info("No students found.")
    else:
        s_id = st.number_input("Enter student ID:", min_value=1, step=1)
        if st.button("Mark Present"):
            if s_id in data:
                data[s_id]["attendance"] += 1
                st.success(
                    f"Attendance recorded for {data[s_id]['name']}. Total: {data[s_id]['attendance']} days."
                )
            else:
                st.error("Student not found.")