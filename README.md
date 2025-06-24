# pac-and-go

This document provides step-by-step instructions to set up and run the project.

## Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package installer)

## Setup Instructions

1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/pac-and-go.git
cd pac-and-go
```

2. Create and activate virtual environment

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
cd core
pip install -r requirements.txt
```

4. Run the development server
```bash
python manage.py migrate
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Development

To create a superuser (admin):
```bash
python manage.py createsuperuser
```

To run tests:
```bash
python manage.py test
```

## Deactivating Virtual Environment

When you're done working on the project:
```bash
deactivate
```
