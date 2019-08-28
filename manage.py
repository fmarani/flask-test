from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from book import create_app
from book.models import db, Book, BookRequest

# sets up the app
app = create_app()

manager = Manager(app)
migrate = Migrate(app, db)

# adds the python manage.py db init, db migrate, db upgrade commands
manager.add_command("db", MigrateCommand)


@manager.command
def dev_server():
    app.run(debug=True, host="0.0.0.0", port=5000)


@manager.command
def prod_server():
    app.run(debug=False)


@manager.command
def recreate_db():
    """
    Recreates a database. This should only be used once
    when there's a new database instance. This shouldn't be
    used when you migrate your database.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """
    Insert some seed data. Use with care.
    """
    new_book = Book(title="4H work week")
    req1 = BookRequest(email="john@john.com", book=new_book)
    req2 = BookRequest(email="jack@jack.com", book=new_book)
    db.session.add_all([new_book, req1, req2])

    new_book = Book(title="6H work week")
    req1 = BookRequest(email="john@john.com", book=new_book)
    req2 = BookRequest(email="zack@zack.com", book=new_book)
    db.session.add_all([new_book, req1, req2])

    db.session.commit()


if __name__ == "__main__":
    manager.run()
