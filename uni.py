import sqlite3
db_connect = sqlite3.connect('database.db')
cursor = db_connect.cursor()
commands_info = {
    "help": "Return info about all commands",
    "new (student, teacher, course, exam, grade)": "Adds new value to the table",
    "edit (student, teacher, course)": "Updates value in the table",
    "delete (student, teacher, course, exam) [id]": "Deletes value from the table",
    "get_course_by_teacher": "Get all courses with teacher with specific id",
    "get_students_by_department": "Get all students with specific department",
    "get_students_by_course": "Get all students on specific course",
    "get_grades_by_course": "Get all grades on specific course",
    "average_of_student_on_course": "Get average grade of a student on specific course",
    "average_of_student": "Get average grade of a student",
    "average_of_dep": "Get average grade of a department",
    "exit": "Exit the program"
}

def execute_command(cmd):
    cmd = cmd.split()
    main_part = cmd[0]
    if main_part == 'help':
        print("\n- Help -")
        for i in commands_info:
            print(f"{i} - {commands_info[i]}")
    
    elif main_part == 'new':
        print(f"\n- Creating new {cmd[1]} -")
        if cmd[1] == "student":
            new_info = input("Enter their info (name, surname, department, date_of_birth) separating values by \", \": ").split(", ")
            cursor.execute("INSERT INTO Students (name, surname, department, date_of_birth) VALUES (?, ?, ?, ?)", new_info)
        elif cmd[1] == "teacher":
            new_info = input("Enter their info (name, surname, department) separating values by \", \": ").split(", ")
            cursor.execute("INSERT INTO Teachers (name, surname, department) VALUES (?, ?, ?)", new_info)
        elif cmd[1] == "course":
            new_info = input("Enter its info (title, description, teacher_id) separating values by \", \": ").split(", ")
            cursor.execute("INSERT INTO Courses (title, description, teacher_id) VALUES (?, ?, ?)", new_info)
        elif cmd[1] == "exam":
            new_info = input("Enter its info (date, max_score, course_id) separating values by \", \": ").split(", ")
            cursor.execute("INSERT INTO Exams (date, max_score, course_id) VALUES (?, ?, ?)", new_info)
        elif cmd[1] == "grade":
            new_info = input("Enter its info (score, student_id, exam_id) separating values by \", \": ").split(", ")
            cursor.execute("INSERT INTO Grades (score, student_id, exam_id) VALUES (?, ?, ?)", new_info)
        else:
            print("Invalid arguments for \"new\" command")
            return
        db_connect.commit()
        print(f"New {cmd[1]} created!")
    
    elif main_part == "get_students_by_department":
        dept = input("\n- Insert department you would like to search for: ")
        cursor.execute("SELECT * FROM Students WHERE department = ?", (dept,))
        data = cursor.fetchall()
        print(f"\n- All students in department \"{dept}\" -")
        for row in data:
            print(f"id: {row[0]} | name: {row[1]} | surname: {row[2]} | department: {row[3]} | date_of_birth: {row[4]}")
    
    elif main_part == "get_course_by_teacher":
        teacher_id = input("\n- Insert teacher ID: ")
        cursor.execute("SELECT * FROM Courses WHERE teacher_id = ?", (teacher_id,))
        data = cursor.fetchall()
        print(f"\n- All courses taught by teacher with ID {teacher_id} -")
        for row in data:
            print(f"id: {row[0]} | title: {row[1]} | description: {row[2]}")
    
    elif main_part == "get_students_by_course":
        course_id = input("\n- Insert course ID: ")
        cursor.execute("""
            SELECT DISTINCT s.* FROM Students s
            JOIN Grades g ON s.id = g.student_id
            JOIN Exams e ON g.exam_id = e.id
            WHERE e.course_id = ?
        """, (course_id,))
        data = cursor.fetchall()
        print(f"\n- All students enrolled in course with ID {course_id} -")
        for row in data:
            print(f"id: {row[0]} | name: {row[1]} | surname: {row[2]} | department: {row[3]} | date_of_birth: {row[4]}")
    
    elif main_part == "get_grades_by_course":
        course_id = input("\n- Insert course ID: ")
        cursor.execute("""
            SELECT s.name, s.surname, e.date, g.score
            FROM Grades g
            JOIN Students s ON g.student_id = s.id
            JOIN Exams e ON g.exam_id = e.id
            WHERE e.course_id = ?
        """, (course_id,))
        data = cursor.fetchall()
        print(f"\n- All grades for course with ID {course_id} -")
        for row in data:
            print(f"Student: {row[0]} {row[1]} | Exam Date: {row[2]} | Score: {row[3]}")
    
    elif main_part == "average_of_student_on_course":
        student_id = input("\n- Insert student ID: ")
        course_id = input("- Insert course ID: ")
        cursor.execute("""
            SELECT AVG(g.score)
            FROM Grades g
            JOIN Exams e ON g.exam_id = e.id
            WHERE g.student_id = ? AND e.course_id = ?
        """, (student_id, course_id))
        avg_grade = cursor.fetchone()[0]
        print(f"\n- Average grade of student {student_id} on course {course_id}: {avg_grade:.2f}")
    
    elif main_part == "average_of_student":
        student_id = input("\n- Insert student ID: ")
        cursor.execute("""
            SELECT AVG(score)
            FROM Grades
            WHERE student_id = ?
        """, (student_id,))
        avg_grade = cursor.fetchone()[0]
        print(f"\n- Average grade of student {student_id}: {avg_grade:.2f}")
    
    elif main_part == "average_of_dep":
        department = input("\n- Insert department name: ")
        cursor.execute("""
            SELECT AVG(g.score)
            FROM Grades g
            JOIN Students s ON g.student_id = s.id
            WHERE s.department = ?
        """, (department,))
        avg_grade = cursor.fetchone()[0]
        print(f"\n- Average grade of department {department}: {avg_grade:.2f}")
    
    elif main_part == "edit":
        id = input(f"\n- Enter the ID of the {cmd[1]} to edit: ")
        if cmd[1] == "student":
            new_info = input("Enter updated info (name, surname, department, date_of_birth) separating values by \", \": ").split(", ")
            cursor.execute("UPDATE Students SET name=?, surname=?, department=?, date_of_birth=? WHERE id=?", (*new_info, id))
        elif cmd[1] == "teacher":
            new_info = input("Enter updated info (name, surname, department) separating values by \", \": ").split(", ")
            cursor.execute("UPDATE Teachers SET name=?, surname=?, department=? WHERE id=?", (*new_info, id))
        elif cmd[1] == "course":
            new_info = input("Enter updated info (title, description, teacher_id) separating values by \", \": ").split(", ")
            cursor.execute("UPDATE Courses SET title=?, description=?, teacher_id=? WHERE id=?", (*new_info, id))
        else:
            print("Invalid table for edit command")
            return
        db_connect.commit()
        print(f"{cmd[1]} with ID {id} updated successfully!")
    
    elif main_part == "delete":
        id = cmd[2] if len(cmd) > 2 else input(f"\n- Enter the ID of the {cmd[1]} to delete: ")
        if cmd[1] == "student":
            cursor.execute("DELETE FROM Students WHERE id=?", (id,))
        elif cmd[1] == "teacher":
            cursor.execute("DELETE FROM Teachers WHERE id=?", (id,))
        elif cmd[1] == "course":
            cursor.execute("DELETE FROM Courses WHERE id=?", (id,))
        elif cmd[1] == "exam":
            cursor.execute("DELETE FROM Exams WHERE id=?", (id,))
        else:
            print("Invalid table for delete command")
            return
        db_connect.commit()
        print(f"{cmd[1]} with ID {id} deleted successfully!")
    elif main_part == "exit":
        return False
    else:
        print("Command does not exist")
    return True

print("Connected to the Main University Database")
print("Type 'help' for a list of commands or 'exit' to quit")

while True:
    if not execute_command(input("> ")):
        break
print("Exiting.")

db_connect.close()
