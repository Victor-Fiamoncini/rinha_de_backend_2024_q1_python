from importlib import import_module
from dynaconf import FlaskDynaconf
from flask import Flask


def load_extensions(app: Flask):
    for extension in app.config["EXTENSIONS"]:
        mod = import_module(extension)
        mod.init_app(app)


def init_app(app: Flask):
    FlaskDynaconf(app, settings_files=["settings.toml"])
