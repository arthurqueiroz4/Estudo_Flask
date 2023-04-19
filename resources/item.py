import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema
blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            return {"message": "Item not found"}, 404

    def delete(self,item_id):
        try:
            items.pop(item_id)
            return {"message":"Item deleted"}
        except KeyError:
            abort(404, message="Item not found")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self,item_data,item_id):  
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, json_item):
        for item in items.values():
            if(
                json_item["name"] == item["name"]
                and json_item["store_id"] == item["store_id"]
            ):
                abort(400, message="Store already registred.")
        if json_item["store_id"] not in stores:
            abort(404, message="Store not found")
        
        item_id = uuid.uuid4().hex
        item = {**json_item, "id":item_id}
        items[item_id] = item
        return item, 201

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return list(items.values())
