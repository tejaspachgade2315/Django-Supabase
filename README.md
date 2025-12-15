# Task Manager - Django + Supabase Demo

A simple task management web application built with Django and PostgreSQL (Supabase), demonstrating CRUD operations, third-party API integration, and data visualization.

## 🌟 Features

- **CRUD API**: Full Create, Read, Update, Delete operations for tasks
- **REST API**: Django REST Framework powered API endpoints
- **Third-party API Integration**: OpenWeatherMap API for weather data
- **Data Visualization**: Interactive charts using Chart.js
- **Responsive Dashboard**: Modern UI with Tailwind CSS
- **Production Ready**: Configured for deployment on Railway/Render

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 5.0
- **Database**: PostgreSQL (Supabase) / SQLite (local)
- **API**: Django REST Framework
- **Frontend**: HTML, Tailwind CSS, Chart.js
- **Deployment**: Gunicorn, WhiteNoise

## 📁 Project Structure

```
supabase-task-manager/
├── config/                 # Django project settings
│   ├── settings.py        # Main configuration
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI application
├── tasks/                  # Tasks application
│   ├── models.py          # Task data model
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   └── urls.py            # API endpoints
├── templates/              # HTML templates
│   └── index.html         # Dashboard template
├── static/                 # Static files
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment configuration
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/supabase-task-manager.git
   cd supabase-task-manager
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   - Dashboard: http://localhost:8000
   - API: http://localhost:8000/api/

## 🔌 API Endpoints

### Tasks CRUD

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/` | List all tasks |
| POST | `/api/tasks/` | Create a new task |
| GET | `/api/tasks/{id}/` | Get task details |
| PUT | `/api/tasks/{id}/` | Update a task |
| DELETE | `/api/tasks/{id}/` | Delete a task |

### Additional Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stats/` | Get task statistics |
| GET | `/api/weather/?city=London` | Get weather data (Third-party API) |

### Example API Requests

**Create a task:**
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Django", "priority": "high", "status": "pending"}'
```

**Get all tasks:**
```bash
curl http://localhost:8000/api/tasks/
```

**Get statistics:**
```bash
curl http://localhost:8000/api/stats/
```

## 🗄️ Database Configuration

### Option 1: SQLite (Default - for local development)
No configuration needed. The app uses SQLite by default.

### Option 2: Supabase PostgreSQL

1. Create a project at [supabase.com](https://supabase.com)
2. Go to Project Settings > Database
3. Copy the connection string
4. Update `.env`:
   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   ```

## 🌐 Deployment

### Deploy to Railway

1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Add environment variables:
   - `SECRET_KEY`: Generate a secure key
   - `DATABASE_URL`: Your Supabase connection string
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.railway.app
4. Deploy!

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`
4. Add environment variables
5. Deploy!

## 🌤️ Third-Party API Integration

This project demonstrates integration with the **OpenWeatherMap API**:

1. Sign up at [openweathermap.org](https://openweathermap.org/api)
2. Get your free API key
3. Add to `.env`:
   ```
   OPENWEATHER_API_KEY=your-api-key
   ```

The weather widget on the dashboard will fetch real weather data.

## 📊 Data Visualization

The dashboard includes two interactive charts:

1. **Status Distribution (Doughnut Chart)**: Shows pending, in-progress, and completed tasks
2. **Priority Distribution (Bar Chart)**: Displays high, medium, and low priority task counts

Both charts update automatically when tasks are added, modified, or deleted.

## 🧪 Testing the API

You can test the API using:

1. **Django REST Framework UI**: Visit `/api/tasks/` in your browser
2. **curl**: Use command-line examples above
3. **Postman/Insomnia**: Import the API endpoints

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | No (default: False) |
| `DATABASE_URL` | Database connection URL | No (default: SQLite) |
| `ALLOWED_HOSTS` | Comma-separated hosts | No |
| `OPENWEATHER_API_KEY` | Weather API key | No (demo mode) |

## 📄 License

MIT License - feel free to use this project for learning or as a starting point.

## 👤 Author

Built as a demo project for Full Stack Developer role assessment.
