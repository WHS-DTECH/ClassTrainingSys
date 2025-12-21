# Class Training System

A comprehensive Flask-based web application for managing programming student training and education.

## Features

- **User Authentication**: Secure login and registration for teachers and students
- **Course Management**: Create and organize programming courses with structured lessons
- **Assignment System**: Submit, grade, and track programming assignments
- **Quiz System**: Create interactive quizzes with automatic grading
- **Progress Tracking**: Monitor student progress across courses and lessons
- **Role-Based Access**: Separate interfaces for teachers and students
- **Responsive Design**: Clean HTML/CSS interface that works on all devices

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **ORM**: Flask-SQLAlchemy

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```powershell
   cd "c:\Users\VanessaPringle.WHS\OneDrive - Westland High School\Documents\web\ClassTrainingSystem"
   ```

2. **Create a virtual environment** (recommended)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```powershell
   python init_db.py
   ```

5. **Run the application**
   ```powershell
   python app.py
   ```

6. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

## Default Accounts

After running `init_db.py`, you'll have these default accounts:

### Teacher Account
- **Username**: teacher
- **Password**: teacher123
- **Email**: teacher@example.com

### Student Account
- **Username**: student
- **Password**: student123
- **Email**: student@example.com

## Project Structure

```
ClassTrainingSystem/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms forms
│   ├── routes/              # Route blueprints
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main/dashboard routes
│   │   ├── courses.py       # Course management
│   │   ├── assignments.py   # Assignment handling
│   │   ├── quizzes.py       # Quiz system
│   │   └── admin.py         # Admin panel
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── courses/
│   │   ├── assignments/
│   │   ├── quizzes/
│   │   └── admin/
│   └── static/              # Static files
│       └── css/
│           └── style.css
├── app.py                   # Application entry point
├── config.py                # Configuration settings
├── init_db.py               # Database initialization script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Usage

### For Teachers

1. **Login** with a teacher account
2. **Create Courses** from the dashboard
3. **Add Lessons** to your courses with content and video links
4. **Create Assignments** for students to complete
5. **Build Quizzes** with multiple question types
6. **Grade Submissions** and provide feedback
7. **Monitor Student Progress** through the admin panel

### For Students

1. **Register** for an account or login
2. **Browse Courses** and enroll
3. **Complete Lessons** and mark them as finished
4. **Submit Assignments** by the due date
5. **Take Quizzes** and receive instant feedback
6. **Track Your Progress** on the dashboard

## Database Schema

The application uses SQLite3 with the following main tables:

- **users**: Student and teacher accounts
- **courses**: Programming courses
- **lessons**: Course content and materials
- **enrollments**: Student course registrations
- **lesson_progress**: Lesson completion tracking
- **assignments**: Programming assignments
- **submissions**: Student assignment submissions
- **quizzes**: Assessment quizzes
- **quiz_questions**: Quiz content
- **quiz_attempts**: Student quiz results

## Development

### Running in Development Mode

```powershell
$env:FLASK_ENV="development"
python app.py
```

The application will run with debug mode enabled and auto-reload on code changes.

### Database Migrations

If you make changes to the models, you can use Flask-Migrate:

```powershell
flask db init
flask db migrate -m "Description of changes"
flask db upgrade
```

## Security Notes

- Change the `SECRET_KEY` in production
- Use environment variables for sensitive configuration
- Implement HTTPS in production
- Add file upload validation for assignments
- Add rate limiting for login attempts

## Future Enhancements

- [ ] File upload support for assignments
- [ ] Real-time notifications
- [ ] Discussion forums
- [ ] Certificate generation
- [ ] Analytics dashboard
- [ ] Email notifications
- [ ] Code syntax highlighting
- [ ] Plagiarism detection
- [ ] Video conferencing integration

## Contributing

This is a school project. For contributions or suggestions, please contact the instructor.

## License

Created for educational purposes at Westland High School.

## Support

For issues or questions, please contact your instructor.
