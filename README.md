getting started without docker
---

make sure you have Postgres installed and a user called "flagz" with password "password". This can easily be changed in book/config.py.

make sure you have a Python3 virtualenv setup, then run the pip commands to install requirements.txt (base stuff) and requirements-dev.txt (dev tools to run tests and so on).

Once you have all that, you can create the db

```
python manage.py recreate_db
python manage.py seed_db
```

and then run the dev server

```
python manage.py dev_server
```

you can run the tests with pytest directly

```
pytest
```

getting started with docker
---

This is enough:

```
docker-compose up
```

It is not possible to run the tests through docker yet as it relies on the Postgres binaries available inside the container, which they are not.


areas of improvement
---

The app is a Flask app with Postgres as storage (and SQLAlchemy as ORM). There is only one component called "book" and its placed in its own folder. Under this folder models and views are in their own folders. I placed all views in the `views/main.py` file although i could have made the name a bit better as the views are all about the request endpoint.

I opted to use a email validator that was already included in Python standard library, although it is very permissive. I think this will need to be replaced for a stricter one.

At this stage the business logic is mixed with the HTTP views layer. In the long term this is not ideal. I would make sure that the two are separated, with inputs/outputs/exceptions properly used and reflecting them in the HTTP payloads and return codes.

The docker setup is not as good as i wanted. I would have used two Dockerfiles (for production and for development) with the development one containing more tools, like the postgres client binaries.
Also this project is not ready to be deployed to production because gunicorn is not hooked up yet.

Seeding the database is not very advanced. I would move the seeding data in a separated file on its own, with a JSON/YAML format, and loaded from there.

Pylint needs to be configured. I would make sure that is run at the end of the test suite, and treat violations as failures. I have not customized much its configuration. I would add some ignore directives, such as line lengths. 

Mypy is also included. It could be beneficial for projects of a certain size to add types and verify the codebase with this tool.

Finally, not much thought has been given to logging and monitoring. When this will be deployed in production, taking care of these 2 aspects will become very important.
