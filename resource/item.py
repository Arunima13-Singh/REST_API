from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cananot be empty')
    parser.add_argument('store_id', type=int, required=True, help='Every Item need a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'No such item exist'}


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'an item with that name {} already exist'.format(name)},400
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except:
            return {'message': 'There is somr problem in inserting the item'}, 500 #int server error
        return item.json(), 200

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json(), 200


    def delete(self, name):
        item =ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Deleted'}

class ItemList(Resource):

    def get(self):
        return {'item':[item.json() for item in ItemModel.query.all()]}



