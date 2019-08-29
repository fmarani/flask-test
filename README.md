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
