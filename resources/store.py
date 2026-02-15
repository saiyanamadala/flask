import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from db import stores

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
  @blp.response(200, StoreSchema(many=True))
  def get(self, store_id):
    return stores.values()

@blp.route("/store")
class StoreNoId(MethodView):
  @blp.response(200, StoreSchema)
  def post(self):
    data = request.get_json()

    if "name" not in data:
      abort(400, message="name not included in the JSON payload")

    for store in stores.values():
      if data["name"] ==store["name"]:
          abort(400, message = "store already exists")

    store_id = uuid.uuid4().hex
    new_store = {**data, "id": store_id}
    stores[store_id] = new_store

    return new_store, 201