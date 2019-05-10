import os
from flask import Flask
from mysite import blog

def create_app():
    app = Flask(__name__)

    # Configure the web app
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "results.db")
        )

    # Register the blue prints of the web app
    app.register_blueprint(blog.bp)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app

app = create_app()

