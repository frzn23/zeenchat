# ZeenChat

A real-time chat application built with Django and Channels.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/frzn23/zeenchat.git
cd zeenchat
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create admin user:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

Access the application at http://127.0.0.1:8000

## Project Structure
```
zeenchat/
├── manage.py
├── zeenchat/
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
└── chatapp/
    ├── views.py
    ├── consumers.py
    ├── routing.py
    ├── templates/
    └── static/
```

## Author
[@frzn23](https://github.com/frzn23)

[LinkedIn](https://www.linkedin.com/in/frzn23/)

## Contact

For questions , contact at [farzeenghaus23@gmail.com](mailto\:farzeenghaus23@gmail.com)


