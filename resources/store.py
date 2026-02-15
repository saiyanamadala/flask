import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
  @blp.response(200, StoreSchema())
  def get(self, store_id):
    item = StoreModel.query.get(store_id)

    return item
  
  def delete(self, store_id):
    item = StoreModel.query.get_or_404(store_id)

    db.session.delete(item)
    db.session.commit()

    return {"message": "store deleted"}

@blp.route("/store")
class StoreNoId(MethodView):
  @blp.arguments(StoreSchema)
  @blp.response(200, StoreSchema)
  def post(self, store_data):
    store = StoreModel(**store_data)
    try:
      db.session.add(store)
      db.session.commit()
    except IntegrityError:
      abort(
        400,
        message = "A store with that name already exists"
      )
    except SQLAlchemyError:
      abort(500, message="An error occured creating the store.")

    return store
  
  @blp.response(200, StoreSchema(many=True))
  def get(self):
    return StoreModel.query.all()