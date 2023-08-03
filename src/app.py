from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/siminar"
app.config["MONGO_URI"] = "mongodb://samit:123456@localhost:27017/pythoneventdb"
mongo = PyMongo(app)


# ส่วนของการ Create Users
@app.route('/users', methods=['POST'])
def create_user():

    # Reciving data
    # return {'message': 'received'}

    fullnname = request.json['fullname']
    email = request.json['email']
    tel = request.json['tel']
    if fullnname and email and tel:
        created_at = request.json['created_at']

        id = mongo.db.users.insert(
            {
                'fullname': fullnname,
                'email': email,
                'tel': tel,
                'created_at': created_at
            }
        )

        response = jsonify({
            '_id': str(id),
            'fullname': fullnname,
            'email': email,
            'tel': tel,
            'created_at': created_at
        })

        response.status_code = 201
        return response

    else:
        return not_found()


# ส่วนของการ GET Users ทั้งหมด
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


# ส่วนของการเรียกดู user ตาม id
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = mongo.db.users.find_one({'_id': ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


# ส่วนของการแก้ไขข้อมูล
@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):

    fullname = request.json['fullname']
    email = request.json['email']
    tel = request.json['tel']

    if fullname and email and tel and _id:
        mongo.db.users.update_one(
            {'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            {'$set': {'fullname': fullname, 'email': email, 'tel': tel}}
        )
        response = jsonify({'message': f'User {_id} Updated Successfuly'})
        response.status_code = 200
        return response
    else:
        return not_found()


# ส่วนของการลบข้อมูล
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': f'User {id} Deleted Successfully'})
    response.status_code = 200
    return response


@app.errorhandler(404)
def not_found(error=None):
    message = {'message': f'Resource Not Found {request.url}', 'status': 404}
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)
