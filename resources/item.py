import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db
from schemas import ItemSchema, ItemUpdateSchema
blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deletado"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data,item_id):  
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(**item_data)
        db.session.add(item)
        db.session.commit()
        return item

@blp.route("/item")
class ItemList(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, json_item):
        item = ItemModel(**json_item)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(
                400, message="Item ja cadastrado"
            )
        except SQLAlchemyError:
            abort(500, message="Erro ao salvar no banco")
        return item

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
