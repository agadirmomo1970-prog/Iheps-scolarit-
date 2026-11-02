"""Point d'entrée WSGI pour Render, VPS, PythonAnywhere, etc."""
from app import create_app

app = create_app()
