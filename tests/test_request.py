from book.models import db, BookRequest, Book


def test_get_request_with_no_id(client):
    rs = client.get("/request")

    assert rs.status_code == 200

    ret_dict = rs.json
    assert ret_dict["data"] == []

    new_book = Book(title="4H work week")
    req1 = BookRequest(email="john@john.com", book=new_book)
    req2 = BookRequest(email="jack@jack.com", book=new_book)
    db.session.add_all([new_book, req1, req2])

    new_book = Book(title="6H work week")
    req1 = BookRequest(email="john@john.com", book=new_book)
    req2 = BookRequest(email="zack@zack.com", book=new_book)
    db.session.add_all([new_book, req1, req2])

    db.session.commit()

    rs = client.get("/request")

    ret_dict = rs.json
    assert len(ret_dict["data"]) == 4
    assert ret_dict["data"][0]["email"] == "john@john.com"  # may fail, fix this


def test_get_request_with_id_404(client):
    rs = client.get("/request/123")
    assert rs.status_code == 404


def test_get_request_with_id_present(client):
    new_book = Book(title="4H work week")
    req1 = BookRequest(email="john@john.com", book=new_book)
    db.session.add_all([new_book, req1])
    db.session.commit()

    rs = client.get("/request/%d" % req1.id)
    assert rs.status_code == 200


def test_post_request_without_title(client):
    rs = client.post("/request", json={"email": "zop@ika.com"})

    assert rs.status_code == 400


def test_post_request_without_valid_email(client):
    new_book = Book(title="4H work week")
    db.session.add_all([new_book])
    db.session.commit()

    rs = client.post(
        "/request", json={"email": "[invalid!email]", "title": "4H work week"}
    )

    assert rs.status_code == 400


def test_post_request_for_book_not_in_db(client):
    rs = client.post(
        "/request", json={"email": "zop@ika.com", "title": "the inexistent"}
    )

    assert rs.status_code == 404


def test_post_request_for_book_in_db(client):
    new_book = Book(title="4H work week")
    db.session.add_all([new_book])
    db.session.commit()

    rs = client.post("/request", json={"email": "zop@ika.com", "title": "4H work week"})

    assert rs.status_code == 200

    ret_dict = rs.json
    assert ret_dict["data"]["email"] == "zop@ika.com"
    assert ret_dict["data"]["title"] == "4H work week"
    assert ret_dict["data"]["id"] is not None
    assert ret_dict["data"]["timestamp"] is not None


def test_delete_request_with_id_404(client):
    rs = client.delete("/request/123")
    assert rs.status_code == 404


def test_delete_request_with_id_present(client):
    new_book = Book(title="4H work week")
    req1 = BookRequest(email="john@john.com", book=new_book)
    db.session.add_all([new_book, req1])
    db.session.commit()

    rs = client.delete("/request/%d" % req1.id)
    assert rs.status_code == 200
