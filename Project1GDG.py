data = dict()


def add_student():
    while True:
        name = input("Enter your name: ").strip()
        if name:
            break
        else:
            print("Name cannot be empty. Please try again.")

    while True:
        try:
            ID = int(input("Enter your ID: "))
            if ID <= 0:
                print("ID must be a positive number. Please try again.")
                continue
            elif ID in data:
                print("ID already exists. Please enter a unique ID.")
                continue
            break
        except ValueError:
            print("ID must be an integer. Please try again.")
            continue

    while True:
        try:
            age = int(input("Enter student age: "))
            if age <= 0:
                print("Age must be greater than 0. Please try again.")
                continue
            break
        except ValueError:
            print("Age must be an integer. Please try again.")
            continue

    grades = []
    for i in range(1, 4):
        while True:
            try:
                grade = float(input(f"Enter grade for Subject {i}: "))
                if grade < 0 or grade > 100:
                    print("Grade must be between 0 and 100. Please try again.")
                    continue
                else:
                    break
            except ValueError:
                print("Grade must be a number. Please try again.")
                continue

        grades.append(grade)

    data[ID] = {"name": name, "age": age, "grades": grades, "attendance": 0}

    print(f"Student {name} with ID {ID} added successfully.")


def view_students():
    if not data:
        print("No students found.")
        return

    sorted_students = sorted(data.items(), key=lambda x: x[1]["name"].lower())

    for index, (ID, info) in enumerate(sorted_students, 1):
        name = info["name"]
        age = info["age"]
        grades = info["grades"]
        attendance = info["attendance"]
        print(
            f"{index}. ID: {ID}, Name: {name}, Age: {age}, Grades: {grades}, Attendance: {attendance} days"
        )


def search_student():
    if not data:
        print("No students found.")
        return

    while True:
        method = input("Search by (1) ID \n\tby (2) Name: ").strip()
        if method == "1":
            try:
                search = int(input("Enter the student ID to search: "))
                if search in data:
                    print(
                        f"Student found: ID: {search}, Name: {data[search]['name']}, Age: {data[search]['age']}, Grades: {data[search]['grades']}, Attendance: {data[search]['attendance']} days"
                    )
                    break
                else:
                    print("Student not found.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid student ID.")
                continue
        elif method == "2":
            search_name = input("Enter the student name to search: ").strip().lower()
            found = False
            for ID, info in data.items():
                if search_name == info["name"].lower():
                    print(
                        f"Student found: ID: {ID}, Name: {info['name']}, Age: {info['age']}, Grades: {info['grades']}, Attendance: {info['attendance']} days"
                    )
                    found = True
            if not found:
                print("Student not found.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def update_grades():
    if not data:
        print("No students found.")
        return

    while True:
        try:
            ID = int(input("Enter the student ID to update grades: "))
        except ValueError:
            print("Invalid input. Please enter a valid student ID.")
            continue

        if ID not in data:
            print("Student not found.")
            break
        else:
            grades = []
            for i in range(1, 4):
                while True:
                    try:
                        grade = float(input(f"Enter new grade for Subject {i}: "))
                        if grade < 0 or grade > 100:
                            print("Grade must be between 0 and 100. Please try again.")
                            continue
                        else:
                            grades.append(grade)
                            break
                    except ValueError:
                        print("Grade must be a number. Please try again.")
                        continue

            data[ID]["grades"] = grades
            print(f"Grades for student ID {ID} updated successfully.")
            print(
                f"Name: {data[ID]['name']}, Age: {data[ID]['age']}, New Grades: {data[ID]['grades']}"
            )
            break


def calculate_average():
    if not data:
        print("No students found.")
        return

    while True:
        try:
            ID = int(input("Enter the student ID to calculate average: "))
            if ID in data:
                grades = data[ID]["grades"]
                average = sum(grades) / len(grades)
                if average >= 90:
                    result = "Excellent"
                elif average >= 80:
                    result = "Very Good"
                elif average >= 70:
                    result = "Good"
                elif average >= 50:
                    result = "Pass"
                else:
                    result = "Fail"
                print(
                    f"Average grade for student ID {ID} ({data[ID]['name']}) is: {average:.2f} ({result})"
                )
                break
            else:
                print("Student not found.")
                break
        except ValueError:
            print("Invalid input. Please enter a valid student ID.")
            continue


def show_top_student():
    if not data:
        print("No students found.")
        return

    top_id = None
    highest_avg = 0

    for ID, info in data.items():
        avg = sum(info["grades"]) / len(info["grades"])
        if avg > highest_avg:
            highest_avg = avg
            top_id = ID

    top_info = data[top_id]
    print(
        f"Top student is ID: {top_id}, Name: {top_info['name']}, Age: {top_info['age']}, Average Grade: {highest_avg:.2f}"
    )


def delete_student():
    if not data:
        print("No students found.")
        return

    while True:
        try:
            ID = int(input("Enter the student ID to delete: "))
            if ID in data:
                del data[ID]
                print(f"Student with ID {ID} deleted successfully.")
                break
            else:
                print("Student not found.")
                continue
        except ValueError:
            print("Invalid input. Please enter a valid student ID.")
            continue


def show_statistics():
    if not data:
        print("No students found.")
        return

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

    total_students = len(data)
    highest_avg = max(averages)
    lowest_avg = min(averages)
    class_avg = sum(averages) / total_students
    passing_percentage = (passing / total_students) * 100

    print(f"Total Students: {total_students}")
    print(f"Highest Average: {highest_avg:.2f}")
    print(f"Lowest Average: {lowest_avg:.2f}")
    print(f"Class Average: {class_avg:.2f}")
    print(f"Passing Students: {passing}")
    print(f"Failing Students: {failing}")
    print(f"Class Passing Percentage: {passing_percentage:.2f}%")


def show_passing_students():
    if not data:
        print("No students found.")
        return

    passing_list = [
        (ID, info)
        for ID, info in data.items()
        if sum(info["grades"]) / len(info["grades"]) >= 50
    ]

    if not passing_list:
        print("No passing students found.")
        return

    for index, (ID, info) in enumerate(passing_list, 1):
        avg = sum(info["grades"]) / len(info["grades"])
        print(f"{index}. ID: {ID}, Name: {info['name']}, Average: {avg:.2f}")


def mark_attendance():
    if not data:
        print("No students found.")
        return

    while True:
        try:
            ID = int(input("Enter the student ID to mark attendance: "))
            if ID in data:
                data[ID]["attendance"] += 1
                print(
                    f"Attendance recorded for {data[ID]['name']}. Total attendance: {data[ID]['attendance']} days."
                )
                break
            else:
                print("Student not found.")
                break
        except ValueError:
            print("Invalid input. Please enter a valid student ID.")
            continue


while True:
    print("\n" + "=" * 33)
    print("   STUDENT MANAGEMENT SYSTEM")
    print("=" * 33)
    print(
        "1. Add a New Student\n"
        "2. View All Students\n"
        "3. Search for a Student\n"
        "4. Update Student Grades\n"
        "5. Calculate Student Average\n"
        "6. Show the Top Student\n"
        "7. Delete a Student\n"
        "8. Show Statistics\n"
        "9. Show Passing Students\n"
        "10. Mark Attendance\n"
        "11. Exit"
    )
    try:
        choice = int(input("\nEnter your choice (1-11): "))
        if choice < 1 or choice > 11:
            raise ValueError
        elif choice == 11:
            print("Exiting...")
            break
        elif choice == 1:
            print()
            print("Adding a new student...".center(50, "-"))
            print()
            add_student()
        elif choice == 2:
            print()
            print("Viewing all students...".center(50, "-"))
            print()
            view_students()
        elif choice == 3:
            print()
            print("Searching for a student...".center(50, "-"))
            print()
            search_student()
        elif choice == 4:
            print()
            print("Updating student grades...".center(50, "-"))
            print()
            update_grades()
        elif choice == 5:
            print()
            print("Calculating student average...".center(50, "-"))
            print()
            calculate_average()
        elif choice == 6:
            print()
            print("Showing the top student...".center(50, "-"))
            print()
            show_top_student()
        elif choice == 7:
            print()
            print("Deleting a student...".center(50, "-"))
            print()
            delete_student()
        elif choice == 8:
            print()
            print("Showing statistics...".center(50, "-"))
            print()
            show_statistics()
        elif choice == 9:
            print()
            print("Showing passing students...".center(50, "-"))
            print()
            show_passing_students()
        elif choice == 10:
            print()
            print("Marking attendance...".center(50, "-"))
            print()
            mark_attendance()
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 11.")
        continue
