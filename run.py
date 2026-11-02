"""Point d'entrée de développement."""
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    production = bool(os.environ.get("RENDER")) or os.environ.get(
        "FLASK_ENV"
    ) == "production"
    if debug and production:
        raise RuntimeError("Le mode debug est interdit en production.")
    app.run(
        host=os.environ.get("HOST", "127.0.0.1"),
        port=int(os.environ.get("PORT", "5000")),
        debug=debug,
    )
