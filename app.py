from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
]

products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99}
]

# User endpoints
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json or 'email' not in request.json:
        return jsonify({"error": "Invalid request"}), 400
    
    new_user = {
        "id": len(users) + 1,
        "name": request.json['name'],
        "email": request.json['email']
    }
    users.append(new_user)
    return jsonify(new_user), 201

# Product endpoints
@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in products if product['id'] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 