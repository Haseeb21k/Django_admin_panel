# Django Blog Platform

This is a full-featured blog platform built with Django. It allows users to create, edit, and delete blog posts, upload images and files, manage profiles, and more. The project is structured for easy development and deployment.

## Features

- User authentication (signup, login, logout)
- Create, edit, and delete blog posts
- Upload images and files to posts
- User profile management
- Responsive HTML templates and custom CSS
- Admin interface for managing content

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default, easy to switch to PostgreSQL/MySQL)
- **Frontend:** Django Templates, HTML, CSS
- **Media Handling:** Django’s built-in media management

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- (Recommended) Virtual environment tool (e.g., `venv`)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install django
   ```

4. **Apply migrations:**
   ```sh
   cd project_1
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure

```
project_root/
│
├── project_1/
│   ├── blog/                # Main Django app
│   ├── project_1/           # Project settings and URLs
│   ├── db.sqlite3           # SQLite database
│   └── manage.py            # Django management script
├── venv/                    # Python virtual environment
└── README.md
```
