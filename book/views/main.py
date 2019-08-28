from flask import Blueprint, request, jsonify
from ..models import db, BookRequest, Book
import logging
from email.utils import parseaddr

logger = logging.getLogger(__name__)
blueprint = Blueprint("book", __name__)


@blueprint.route("/request", methods=["GET"])
def get_requests():
    requests = BookRequest.query.join(Book).all()
    response = {"data": [i.to_dict() for i in requests]}
    return jsonify(response), 200


@blueprint.route("/request/<r_id>", methods=["GET"])
def get_request(r_id):
    request = BookRequest.query.filter_by(id=r_id).first()

    if request:
        response = {"data": request.to_dict()}
        return jsonify(response), 200
    else:
        return jsonify({}), 404


@blueprint.route("/request", methods=["POST"])
def create_request():
    data = request.get_json()

    logger.info("Data recieved: %s", data)
    if "title" not in data:
        msg = "No book title provided for book request."
        logger.info(msg)
        return jsonify({"message": msg}), 400
    if "email" not in data:
        msg = "No email provided for book request."
        logger.info(msg)
        return jsonify({"message": msg}), 400

    book = Book.query.filter_by(title=data["title"]).first()
    if not book:
        msg = "No book found with given title."
        logger.info(msg)
        return jsonify({"message": msg}), 404

    email = parseaddr(data["email"])[1]
    if not email:
        msg = "No valid email submitted."
        logger.info(msg)
        return jsonify({"message": msg}), 400

    new_request = BookRequest(email=email, book=book)
    db.session.add(new_request)
    db.session.commit()

    response = {"data": new_request.to_dict()}
    return jsonify(response), 200


@blueprint.route("/request/<r_id>", methods=["DELETE"])
def delete_request(r_id):
    db_request = BookRequest.query.filter_by(id=r_id).first()

    if db_request:
        db.session.delete(db_request)
        db.session.commit()
        return "", 200
    else:
        return "", 404
