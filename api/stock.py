import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource  # Used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import db, Post  # Import your database setup and Post model
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.users import db, Post  # Adjust import as necessary
from sqlalchemy.exc import IntegrityError
# api/stock.py

# ... Your existing imports ...

stock_api = Blueprint('stock_api', __name__, url_prefix='/api/stock')
api = Api(stock_api)

class StockList(Resource):
    def post(self):
        data = request.get_json()
        new_stock = Post(
            company_name=data['company_name'],
            shares=data['shares'],
            purchase_price=data['purchase_price'],
            current_price=data.get('current_price'),  # Accept current_price from the request
            userID=data.get('userID')  # Assuming userID is provided in the request body
        )
        db.session.add(new_stock)
        try:
            db.session.commit()
            return {"message": "Stock added"}, 201
        except IntegrityError as e:
            db.session.rollback()
            return {"message": str(e)}, 400

    def get(self):
        stocks = Post.query.all()
        stock_list = [
            {
                'id': stock.id,
                'company_name': stock.company_name,
                'shares': stock.shares,
                'purchase_price': stock.purchase_price,
                'current_price': stock.current_price,  # Include current_price in the response
                'userID': stock.userID
            } for stock in stocks
        ]
        return stock_list, 200

api.add_resource(StockList, '/stocks')

# ... Rest of your file ...
