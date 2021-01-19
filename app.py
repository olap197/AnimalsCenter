from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, String, Column
import uuid
import jwt
import datetime
import logging
from sqlalchemy.sql import func
from functools import wraps
logging.basicConfig(filename='demo.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db' # new
app.config['SECRET_KEY']='Th1s1ss3cr3t'
secret=app.config['SECRET_KEY']
print(secret)

class AccessRequest(db.Model):
    ar_id=db.Column(db.Integer, primary_key=True)
    c_id = db.Column(db.Integer, nullable=False)
    timestamp = Column(db.DateTime(timezone=True), server_default=func.now())


class Center(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    
class Animals(db.Model):
    a_id = db.Column(db.Integer, primary_key=True, index=True)
    centerid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    #species = db.Column(db.String(50), nullable=False, ForeignKey("species.name"))
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=True)
    species = db.Column(db.String(50), nullable=True)


class Species(db.Model):
    s_id = db.Column(db.Integer, primary_key=True, index=True)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=True)
    name = db.Column(db.String(50), nullable=False)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms="HS256")
            current_user = Center.query.filter_by(c_id=data['c_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator
@app.route('/register', methods=['POST'])
def create_user():
    data=request.get_json()
    u=Center(
        login=data['login'],
        password=data['password'],
        address=data['address']
    )
    app.logger.info("New user registered")
    db.session.add(u)
    db.session.commit()
    return{
        'c_id':u.c_id,'login':u.login, 'password':u.password,'address':u.address
    },201

@app.route('/login', methods=['GET', 'POST'])   
def login_user(): 
 
  auth = request.authorization   

  if not auth or not auth.username or not auth.password:  
     return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

  center = Center.query.filter_by(login=auth.username).first()
  ar=AccessRequest(
      c_id=center.c_id,
      timestamp=datetime.datetime.now()
  )
  
  db.session.add(ar)
  db.session.commit()
  print(ar.c_id, ar.timestamp)  
  print(center.c_id) 
  app.logger.info(center.login," Logged in")
  if (str(center.password) == str(auth.password)):  
     token =  jwt.encode(
            {"c_id":center.c_id},
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )  
     print(token.encode('UTF-8'))
     return jsonify({'token' : token}) 
  return ('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/animals', methods=['POST'])
@token_required
def create_animal(current_user):
    
    data=request.get_json()
    u=Animals(
        centerid=current_user.c_id,
        name=data['name'],
        age=data['age'],
        price=data['price'],
        species=data['species']

    )
    db.session.add(u)
    db.session.commit()
    app.logger.info(u.centerid,u.name," Animal added")
    return{
        'a_id':u.a_id,'centerid':u.centerid, 
        'name':u.name,'age':u.age,'price':u.price,
        'species':u.species
    },201


@app.route('/species', methods=['POST'])
@token_required
def create_specie(current_user):
    data=request.get_json()
    u=Species(
        s_id=data['s_id'],
        description=data['description'],
        name=data['name'],
        price=data['price']

    )
    db.session.add(u)
    db.session.commit()
    app.logger.info(u.s_id,u.name," Species added")
    return{
        's_id':u.s_id,'description':u.description,
         'name':u.name,'price':u.price
    },201



@app.route('/center', methods=['GET'])
def read_users():
    return jsonify([{
        'c_id':u.c_id,'login':u.login, 'password':u.password,'address':u.address
    }for u in Center.query.all()
    ])
@app.route('/center/<id>/')
def get_user(id):
	print(id)
	u = Center.query.filter_by(c_id=id).first_or_404()
	return {
		'c_id':u.c_id,'login':u.login, 'password':u.password,'address':u.address
		}


@app.route('/animals', methods=['GET'])
def read_animals():
    return jsonify([{
        'a_id':a.a_id,'centerid':a.centerid, 
        'name':a.name,'age':a.age,'price':a.price,
        'species':a.species
    }for a in Animals.query.all()
    ])
@app.route('/animals/<id>/', methods=['GET'])
def get_animal(id):
	print(id)
	a = Animals.query.filter_by(a_id=id).first_or_404()
	return {
		'a_id':a.a_id,'centerid':a.centerid, 
        'name':a.name,'age':a.age,'price':a.price,
        'species':a.species
		}
@app.route('/animals/<animal_id>/', methods=['PUT'])
@token_required
def update_animal(current_user,animal_id):
	data = request.get_json()
	if 'name' not in data:
		return {
			'error': 'Bad Request',
			'message': 'Name field needs to be present'
		}, 400
	a = Animals.query.filter_by(a_id=animal_id).first_or_404()
	db.session.commit()
    #app.logger.info("animal updated",a.a_id,a.name)
    
	return jsonify({
		'a_id':a.a_id,'centerid':a.centerid, 
        'name':a.name,'age':a.age,'price':a.price,
        'species':a.species
	}),201


@app.route('/animals/<animal_id>/', methods=['DELETE'] )
#@token_required
def delete_animal(animal_id):
	animal = Animals.query.filter_by(a_id=animal_id).first_or_404()
	db.session.delete(animal)
	db.session.commit()
	return {
		'success': 'Data deleted successfully'
	}


@app.route('/species', methods=['GET'])
def read_species():
    return jsonify([{
        's_id':s.s_id,'description':s.description,
         'name':s.name,'price':s.price
    }for s in Species.query.all()
    ])
@app.route('/species/<id>/')
def get_specie(id):
	print(id)
	s = Species.query.filter_by(s_id=id).first_or_404()
	return {
		's_id':s.s_id,'description':s.description,
         'name':s.name,'price':s.price
		}

if __name__ == '__main__':
    app.run(debug=True)

