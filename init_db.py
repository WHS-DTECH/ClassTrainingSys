"""
Database initialization script
Creates database tables and populates with sample data
"""

from app import create_app, db
from app.models import User, Course, Lesson, Assignment, Quiz, QuizQuestion, Enrollment
from datetime import datetime, timedelta

def init_database():
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating tables...")
        db.create_all()
        
        # Create sample users
        print("Creating sample users...")
        
        # Teacher
        teacher = User(
            username='teacher',
            email='teacher@example.com',
            first_name='John',
            last_name='Smith',
            role='teacher'
        )
        teacher.set_password('teacher123')
        db.session.add(teacher)
        
        # Students
        student1 = User(
            username='student',
            email='student@example.com',
            first_name='Jane',
            last_name='Doe',
            role='student'
        )
        student1.set_password('student123')
        db.session.add(student1)
        
        student2 = User(
            username='alice',
            email='alice@example.com',
            first_name='Alice',
            last_name='Johnson',
            role='student'
        )
        student2.set_password('alice123')
        db.session.add(student2)
        
        db.session.commit()
        print(f"Created users: teacher, student, alice")
        
        # Create sample course
        print("Creating sample course...")
        course = Course(
            title='Introduction to Python Programming',
            description='Learn the fundamentals of Python programming including variables, loops, functions, and object-oriented programming.',
            teacher_id=teacher.id
        )
        db.session.add(course)
        db.session.commit()
        
        # Create sample lessons
        print("Creating sample lessons...")
        lessons_data = [
            {
                'title': 'Getting Started with Python',
                'content': '<h2>Welcome to Python!</h2><p>Python is a powerful, easy-to-learn programming language. In this lesson, you\'ll learn how to install Python and write your first program.</p><pre>print("Hello, World!")</pre>',
                'order': 1
            },
            {
                'title': 'Variables and Data Types',
                'content': '<h2>Variables and Data Types</h2><p>Learn about Python\'s basic data types including strings, integers, floats, and booleans.</p><pre>name = "Alice"\nage = 25\nis_student = True</pre>',
                'order': 2
            },
            {
                'title': 'Control Flow: If Statements',
                'content': '<h2>Conditional Statements</h2><p>Learn how to make decisions in your code using if, elif, and else statements.</p><pre>if age >= 18:\n    print("Adult")\nelse:\n    print("Minor")</pre>',
                'order': 3
            },
            {
                'title': 'Loops in Python',
                'content': '<h2>For and While Loops</h2><p>Master iteration in Python using for and while loops.</p><pre>for i in range(5):\n    print(i)</pre>',
                'order': 4
            },
            {
                'title': 'Functions',
                'content': '<h2>Creating Functions</h2><p>Learn how to organize your code using functions.</p><pre>def greet(name):\n    return f"Hello, {name}!"</pre>',
                'order': 5
            }
        ]
        
        for lesson_data in lessons_data:
            lesson = Lesson(
                course_id=course.id,
                **lesson_data
            )
            db.session.add(lesson)
        
        db.session.commit()
        print(f"Created {len(lessons_data)} lessons")
        
        # Enroll students in ALL courses
        print("Enrolling students in all courses...")
        all_courses = Course.query.all()
        all_students = User.query.filter_by(role='student').all()
        
        for student in all_students:
            for course_obj in all_courses:
                # Check if enrollment already exists
                existing = Enrollment.query.filter_by(
                    student_id=student.id,
                    course_id=course_obj.id
                ).first()
                
                if not existing:
                    enrollment = Enrollment(student_id=student.id, course_id=course_obj.id)
                    db.session.add(enrollment)
        
        db.session.commit()
        print(f"Enrolled {len(all_students)} students in {len(all_courses)} courses")
        
        # Create sample assignment
        print("Creating sample assignment...")
        assignment = Assignment(
            course_id=course.id,
            title='Variables and Data Types Exercise',
            description='Create a Python program that uses different data types and prints their values.',
            due_date=datetime.utcnow() + timedelta(days=7),
            max_points=100
        )
        db.session.add(assignment)
        db.session.commit()
        
        # Create sample quiz
        print("Creating sample quiz...")
        quiz = Quiz(
            course_id=course.id,
            title='Python Basics Quiz',
            description='Test your knowledge of Python fundamentals',
            time_limit=30,
            max_attempts=2
        )
        db.session.add(quiz)
        db.session.commit()
        
        # Add quiz questions
        questions_data = [
            {
                'question_text': 'What is the correct way to print "Hello" in Python?',
                'question_type': 'multiple_choice',
                'options': 'echo("Hello")\nprint("Hello")\nconsole.log("Hello")\nSystem.out.println("Hello")',
                'correct_answer': 'print("Hello")',
                'points': 10,
                'order': 1
            },
            {
                'question_text': 'Python is a case-sensitive language',
                'question_type': 'true_false',
                'options': 'True\nFalse',
                'correct_answer': 'True',
                'points': 10,
                'order': 2
            },
            {
                'question_text': 'Which data type is used to store whole numbers?',
                'question_type': 'short_answer',
                'correct_answer': 'int',
                'points': 10,
                'order': 3
            }
        ]
        
        for q_data in questions_data:
            question = QuizQuestion(
                quiz_id=quiz.id,
                **q_data
            )
            db.session.add(question)
        
        db.session.commit()
        print(f"Created quiz with {len(questions_data)} questions")
        
        print("\n" + "="*60)
        print("Database initialized successfully!")
        print("="*60)
        print("\nDefault accounts created:")
        print("\nTeacher Account:")
        print("  Username: teacher")
        print("  Password: teacher123")
        print("  Email: teacher@example.com")
        print("\nStudent Account:")
        print("  Username: student")
        print("  Password: student123")
        print("  Email: student@example.com")
        print("\nStudent Account 2:")
        print("  Username: alice")
        print("  Password: alice123")
        print("  Email: alice@example.com")
        print("\n" + "="*60)

if __name__ == '__main__':
    init_database()
