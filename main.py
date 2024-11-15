from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Lista simulando una base de datos
users = [
    {"id": 1, "name": "Sthephany", "lastname": "Toribio"},
    {"id": 5, "name": "Edwin", "lastname": "Jara"}
]

# Ruta para obtener la lista completa de usuarios o un usuario por query parameter ?user=<id>
@app.route('/users', methods=['GET'])
def get_users():
    user_id = request.args.get('user')  # Obtener el parámetro user de la URL
    if user_id:
        user = next((user for user in users if user["id"] == int(user_id)), None)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user)
    return jsonify(users)

'''
# Ruta para agregar un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    if not request.json or 'name' not in request.json or 'lastname' not in request.json:
        return abort(400)  # Bad request si faltan datos

    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,  # Auto-generar ID
        "name": request.json["name"],
        "lastname": request.json["lastname"]
    }
    users.append(new_user)
    return jsonify(new_user), 201
'''

# Ruta para agregar un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    user_name = request.args.get('name')
    user_lastname = request.args.get('lastname')
    if user_name and user_lastname:
        new_user = {
            "id": users[-1]["id"] + 1 if users else 1,  # Auto-generar ID
            "name": user_name,
            "lastname": user_lastname
        }
        users.append(new_user)
        return jsonify(new_user), 201
    else:
        return abort(400)  # Bad request si faltan datos


# Ruta para actualizar un usuario existente por query parameter ?user=<id>
@app.route('/users', methods=['PUT'])
def update_user():
    user_id = request.args.get('user')  # Obtener el parámetro user de la URL
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = next((user for user in users if user["id"] == int(user_id)), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404


    user['name'] = request.args.get('name')
    user['lastname'] = request.args.get('lastname')

    return jsonify(user)


# Ruta para eliminar un usuario por query parameter ?user=<id>
@app.route('/users', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('user')  # Obtener el parámetro user de la URL
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    user = next((user for user in users if user["id"] == int(user_id)), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    users.remove(user)
    return jsonify({"result": True})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
