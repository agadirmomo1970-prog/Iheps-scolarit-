"""Initialise la base IHEPS AGADIR : paramètres et compte administrateur.

Usage : python seed.py
"""
from app import create_app
from app.seed import ensure_base_data


def main() -> None:
    app = create_app()
    with app.app_context():
        ensure_base_data()
        print("Base de données initialisée : paramètres et compte administrateur.")


if __name__ == "__main__":
    main()
