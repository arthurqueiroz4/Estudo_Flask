import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from models import StoreModel
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deletado"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema) 
    def post(self, request_data):
        store = StoreModel(**request_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400, message="Store ja cadastrado"
            )
        except SQLAlchemyError:
            abort(500, message="Erro ao salvar no banco")
        return store

    @blp.response(201, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

