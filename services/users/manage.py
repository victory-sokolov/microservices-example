import unittest

from colour_runner import runner
from flask import Flask
from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("seed_db")
def seed_db():
    """Add initial data to the database."""
    db.session.add(User(username="viktor", email="viktorsokolov.and@gmail.com"))
    db.session.add(User(username="nick", email="nick@gmail.com"))
    db.session.commit()


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("test")
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover("project/tests", pattern="test*.py")
    result = runner.ColourTextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    cli()
