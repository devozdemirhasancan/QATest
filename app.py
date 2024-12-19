from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='QA Test API',
          description='A simple API for QA testing purposes',
          doc='/')

# Namespaces
ns_users = api.namespace('api/users', description='User operations')
ns_products = api.namespace('api/products', description='Product operations')
ns_locations = api.namespace('api/locations', description='Location operations')
ns_tariffs = api.namespace('api/tariffs', description='Tariff operations')

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

location_model = api.model('Location', {
    'id': fields.String(readonly=True, description='Location identifier'),
    'evse': fields.String(description='EVSE identifier'),
    'connector': fields.String(description='Connector identifier'),
    'latitude': fields.Float(description='Location latitude'),
    'longitude': fields.Float(description='Location longitude'),
    'radius': fields.Float(description='Search radius in meters')
})

tariff_model = api.model('Tariff', {
    'id': fields.String(readonly=True, description='Tariff identifier'),
    'name': fields.String(description='Tariff name'),
    'price': fields.Float(description='Price per kWh'),
    'currency': fields.String(description='Currency code'),
    'ocpi_compliant': fields.Boolean(description='OCPI compliance status')
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

locations = [
    {
        "id": "102",
        "evse": "DemoCharger12",
        "connector": "14539",
        "latitude": 51.5479372392014,
        "longitude": -0.2841902973282122,
        "radius": 10000
    }
]

tariffs = [
    {
        "id": "GRL1000_10_EST",
        "name": "Standard Tariff",
        "price": 0.35,
        "currency": "EUR",
        "ocpi_compliant": True
    }
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

@ns_locations.route('/')
class LocationList(Resource):
    @ns_locations.doc('list_locations')
    @ns_locations.marshal_list_with(location_model)
    def get(self):
        """List all locations"""
        # Get query parameters
        evse = request.args.get('evse')
        connector = request.args.get('connector')
        lat = request.args.get('lat')
        lon = request.args.get('lon')
        radius = request.args.get('radius')

        if evse or connector:
            filtered_locations = [loc for loc in locations 
                               if (not evse or loc['evse'] == evse) and 
                               (not connector or loc['connector'] == connector)]
            return filtered_locations, 200

        if lat and lon and radius:
            # In a real application, you would implement proper geo-search
            return locations, 200

        return locations, 200

@ns_locations.route('/<string:location_id>')
@ns_locations.response(404, 'Location not found')
class Location(Resource):
    @ns_locations.doc('get_location')
    @ns_locations.marshal_with(location_model)
    def get(self, location_id):
        """Get a specific location by ID"""
        location = next((loc for loc in locations if loc['id'] == location_id), None)
        if location is None:
            api.abort(404, "Location not found")
        return location

@ns_tariffs.route('/')
class TariffList(Resource):
    @ns_tariffs.doc('list_tariffs')
    @ns_tariffs.marshal_list_with(tariff_model)
    def get(self):
        """List all tariffs"""
        return tariffs

@ns_tariffs.route('/<string:tariff_id>')
@ns_tariffs.response(404, 'Tariff not found')
class Tariff(Resource):
    @ns_tariffs.doc('get_tariff')
    @ns_tariffs.marshal_with(tariff_model)
    def get(self, tariff_id):
        """Get a specific tariff by ID"""
        tariff = next((t for t in tariffs if t['id'] == tariff_id), None)
        if tariff is None:
            api.abort(404, "Tariff not found")
        return tariff

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000) 