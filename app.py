from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='QA Test API',
          description='A simple API for QA testing purposes',
          doc='/')

# Namespaces
ns_users = api.namespace('api/users', description='User operations')
ns_products = api.namespace('api/products', description='Product operations')

# Models
user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='User identifier'),
    'name': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email')
})

product_model = api.model('Product', {
    'id': fields.Integer(readonly=True, description='Product identifier'),
    'name': fields.String(required=True, description='Product name'),
    'price': fields.Float(required=True, description='Product price')
})

# Mock database
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99}
]

@ns_users.route('/')
class UserList(Resource):
    @ns_users.doc('list_users')
    @ns_users.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return users

    @ns_users.doc('create_user')
    @ns_users.expect(user_model)
    @ns_users.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        if not request.json or 'name' not in request.json or 'email' not in request.json:
            api.abort(400, "Invalid request")
        
        new_user = {
            "id": len(users) + 1,
            "name": request.json['name'],
            "email": request.json['email']
        }
        users.append(new_user)
        return new_user, 201

@ns_users.route('/<int:user_id>')
@ns_users.response(404, 'User not found')
class User(Resource):
    @ns_users.doc('get_user')
    @ns_users.marshal_with(user_model)
    def get(self, user_id):
        """Get a specific user by ID"""
        user = next((user for user in users if user['id'] == user_id), None)
        if user is None:
            api.abort(404, "User not found")
        return user

@ns_products.route('/')
class ProductList(Resource):
    @ns_products.doc('list_products')
    @ns_products.marshal_list_with(product_model)
    def get(self):
        """List all products"""
        return products

@ns_products.route('/<int:product_id>')
@ns_products.response(404, 'Product not found')
class Product(Resource):
    @ns_products.doc('get_product')
    @ns_products.marshal_with(product_model)
    def get(self, product_id):
        """Get a specific product by ID"""
        product = next((product for product in products if product['id'] == product_id), None)
        if product is None:
            api.abort(404, "Product not found")
        return product

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) 