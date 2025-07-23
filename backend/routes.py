from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500 

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data and type(id) == int:
        for image in data:
            if image["id"] == id:
                return jsonify(image), 200

    return {"message": "Not Found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()

    if picture not in data:
        data.append(picture)
        return jsonify(picture), 201
    elif picture in data:
        return {"Message": f"picture with id {picture['id']} already present"}, 302
 

    return {"message": "Internal server error"}, 500 


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()

    for p in data:
        if p["id"] == id:
            p["pic_url"] = picture.get("pic_url", p.get("pic_url"))
            p["event_country"] = picture.get("event_country", p.get("event_country"))
            p["event_state"] = picture.get("event_state", p.get("event_state"))
            p["event_city"] = picture.get("event_city", p.get("event_city"))
            p["event_date"] = picture.get("event_date", p.get("event_date"))
            return jsonify(p), 200

    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for p in data:
        if p["id"] == id:
            data.remove(p)
            return {}, 204
    return {"message": "picture not found"}, 404

