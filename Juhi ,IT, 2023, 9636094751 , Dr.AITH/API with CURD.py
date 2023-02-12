from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
from werkzeug import generate_password_hash, check_password_hash
import pandas as pd

@app.route('/add', methods=['POST'])
def add_customer():
	_json = request.json
	_name = _json['name']
	_role = _json['role']
	_password = _json['pwd']
	# validate the received values
	if _name and _password and _role and request.method == 'POST':
		#do not save password as a plain text
		_hashed_password = generate_password_hash(_password)
		# save details
		id = mongo.db.customer.insert({'name': _name,'pwd': _hashed_password,'role': _role})
		resp = jsonify('Customer added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/customers')
def customers():
	customers = mongo.db.customer.find()
	resp = dumps(customers)
	return resp
		
@app.route('/customer/<id>')
def customer(id):
	customer = mongo.db.customer.find_one({'_id': ObjectId(id)})
	resp = dumps(customer)
	return resp

@app.route('/update', methods=['PUT'])
def update_customer():
	_json = request.json
	_id = _json['_id']
	_name = _json['name']
	_role = _json['role']
	_password = _json['pwd']		
	# validate the received values
	if _name and _role and _password and _id and request.method == 'PUT':
		#do not save password as a plain text
		_hashed_password = generate_password_hash(_password)
		# save edits
		mongo.db.customer.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'name': _name, 'role': _role, 'pwd': _hashed_password}})
		resp = jsonify('Customer updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/delete/<id>', methods=['DELETE'])
def delete_customer(id):
	mongo.db.customer.delete_one({'_id': ObjectId(id)})
	resp = jsonify('Customer deleted successfully!')
	resp.status_code = 200
	return resp
@app.route('/csv')	
def csv(querry{}):
    # Make a query to the specific DB and Collection
    cursor = db[customer].find(querry)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))
    
    df.to_csv('1.csv', index=False)
    # Delete the _id
    return df

    	
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if name == "main":
    app.run()
