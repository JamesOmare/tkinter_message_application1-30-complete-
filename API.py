from datetime import datetime
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from mysqlx import Session
from flask_session import Session
from html5lib import serialize
from itsdangerous import Serializer
from marshmallow import Schema, fields
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import desc
from flask_migrate import Migrate
import threading
import time

app = Flask(__name__)

#database user:password@hostname/database name
app.config["SECRET_KEY"] = 'jisungparkfromdeep'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://james:foxtrot09er@localhost/test' 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

app.config["SESSION_TYPE"] = db
sess = Session(app)

migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer(), nullable = False)
    gender = db.Column(db.String(50), nullable = False)
    county = db.Column(db.String(60), nullable = False)
    town = db.Column(db.String(60), nullable = False)
    education_level = db.Column(db.String(50), nullable = True)
    profession = db.Column(db.String(60), nullable = True)
    marital_status = db.Column(db.String(50), nullable = True)
    religion = db.Column(db.String(50), nullable = True)
    tribe = db.Column(db.String(50),nullable = True)
    description = db.Column(db.String(100), nullable = True)
    status = db.Column(db.String(100), nullable = True)
    datetime = db.Column(db.DateTime(timezone=True), nullable = False, server_default=func.now())

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()   
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    # @classmethod
    # def get_by_name(cls, name):
    #     return cls.query.get_or_404(name)

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name = name).first()




    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    age = fields.Integer()
    gender = fields.String()
    county = fields.String()
    town = fields.String()
    education_level = fields.String()
    profession = fields.String()
    marital_status = fields.String()
    religion = fields.String()
    tribe = fields.String()
    description = fields.String()
    status = fields.String()
    datetime = fields.DateTime()

class Message(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    header = db.Column(db.String(50), nullable = True)
    sender_number = db.Column(db.Integer(), nullable = False)
    message = db.Column(db.String(160), nullable = False)
    receiver_shortcode = db.Column(db.Integer(), nullable = False)
    datetime = db.Column(db.DateTime(timezone=True), nullable = False, server_default=func.now())

    def __repr__(self):
        return self.sender_number

    @classmethod
    def get_all(cls):
        return cls.query.all()   
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id) 

    @classmethod
    def get_by_sender_number(cls, sender_number):
        return cls.query.filter_by(sender_number = sender_number).first()



        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def last_inserted_row(self):
        db.session.add(self)
        db.session.flush(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class MessageSchema(Schema):
    id = fields.Integer()
    header = fields.String()
    sender_number = fields.Integer()
    message = fields.String()
    receiver_shortcode = fields.Integer()
    datetime = fields.DateTime()


class Penzi(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    message = db.Column(db.String(500), nullable = False)
    shortcode = db.Column(db.Integer(), nullable = False)
    datetime = db.Column(db.DateTime(timezone=True), nullable = False, server_default=func.now())

    def __repr__(self):
        return self.shortcode

    @classmethod
    def get_all(cls):
        return cls.query.all()   
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id) 

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PenziSchema(Schema):
    id = fields.Integer()
    message = fields.String()
    shortcode = fields.Integer()
    datetime = fields.DateTime()


@app.route("/get_all_posts", methods = ["GET"])
def get_all_recipes():

    recipes = User.get_all()
    serializer = User(many=True)
    data = serializer.dump(recipes)

    return jsonify(
        data
    )

@app.route("/post", methods = ["POST"])
def create_user():
    user_data = request.get_json()
    message_data = request.get_json()

    message_m = Message(

        header = message_data.get("header"),
        sender_number = message_data.get("sender_number"),
        message = message_data.get("message"),
        receiver_shortcode = message_data.get("receiver_shortcode")

    )

    message_m.save()
    serializer = MessageSchema()
    message_data = serializer.dump(message_m)

    user_u = User(
       
        name = user_data.get("name"),
        age = user_data.get("age"),
        gender = user_data.get("gender"),
        county = user_data.get("county"),
        town = user_data.get("town"),
        education_level = user_data.get("education_level"),
        profession = user_data.get("profession"),
        marital_status = user_data.get("marital_status"),
        religion = user_data.get("religion"),
        tribe = user_data.get("tribe"),
        description = user_data.get("description")
       
    )

    user_u.save()
    serializer = UserSchema()
    user_data = serializer.dump(user_u)

    
    return jsonify(message_data) and jsonify(user_data), 201


@app.route("/post_penzi", methods = ["POST"])
def post_penzi():
    penzi_data = request.get_json()

    penzi_m = Penzi(

        
        shortcode = penzi_data.get("shortcode"),
        message = penzi_data.get("message")

    )

    penzi_m.save()
    serializer = PenziSchema()
    penzi_data = serializer.dump(penzi_m)

    return jsonify(penzi_data), 201


@app.route("/post_start", methods = ["POST"])
def post_start():
    message_data = request.get_json()

    message_m = Message(

        header = message_data.get("header"),
        sender_number = message_data.get("sender_number"),
        message = message_data.get("message"),
        receiver_shortcode = message_data.get("receiver_shortcode")

    )

    message_m.save()
    serializer = MessageSchema()
    message_data = serializer.dump(message_m)
    return jsonify(message_data), 201


@app.route("/update/<int:id>", methods = ["POST"])
def update_penzi(id):
    update_data = request.get_json(id)

    status_update = User(

        
        status = update_data.get("status")

    )

    status_update.save()
    serializer = PenziSchema()
    update_data = serializer.dump(status_update)

    return jsonify(update_data), 201



@app.route("/get_post_by_user/<int:id>", methods = ["GET"])
def get_post_by_user(id):
    recipe = User.get_by_id(id)
    serializer = UserSchema()
    data = serializer.dump(recipe)
    

    return jsonify(data), 200

def sleep():
    time.sleep(10)

@app.route("/get_penzi_message_start/<int:id>", methods = ["GET"])
def get_penzi_message_start(id):
    message_id = Penzi.get_by_id(id)
    Serializer = PenziSchema()
    data = Serializer.dump(message_id)

    sleep()

    return data.get("message"), 200

@app.route("/get_message/<int:sender_number>", methods = ["GET"])
def get_message(sender_number):
    serial_query = Message.get_by_sender_number(sender_number)
    Serializer = MessageSchema()
    data = Serializer.dump(serial_query)

    return data.get("message"), 200


@app.route("/post_start_user", methods = ["POST"])
def post_start_user():
    user_data = request.get_json()
    user_m = User(

        
        name = user_data.get("name"),
        age = user_data.get("age"),
        gender = user_data.get("gender"),
        county = user_data.get("county"),
        town = user_data.get("town")

    )

    user_m.save()
    serializer = UserSchema()
    user_data = serializer.dump(user_m)
    return jsonify(user_data), 201




@app.route("/patch_user_details/<string:name>", methods = ["PUT"])
def update_user_details(name):
    user_to_update = User.get_by_name(name)

    data= request.get_json()

    user_to_update.education_level = data.get("education_level")
    user_to_update.profession = data.get("profession")
    user_to_update.marital_status = data.get("marital_status")
    user_to_update.religion = data.get("religion")
    user_to_update.tribe = data.get("tribe")
    
    

    db.session.commit()

    Serializer = UserSchema()

    recipe_data = Serializer.dump(user_to_update)

    return jsonify(recipe_data), 200



@app.route("/update_status/<string:name>", methods = ["PUT"])
def update_status(name):
    user_to_update = User.get_by_name(name)

    data= request.get_json()

    user_to_update.education_level = data.get("education_level")
    user_to_update.profession = data.get("profession")
    user_to_update.marital_status = data.get("marital_status")
    user_to_update.religion = data.get("religion")
    user_to_update.tribe = data.get("tribe")
    
    

    db.session.commit()

    Serializer = UserSchema()

    recipe_data = Serializer.dump(user_to_update)

    return jsonify(recipe_data), 200





@app.route("/patch/<int:id>", methods = ["PATCH"])
def update_user(id):
    penzi_data = request.get_json()

    penzi_m = User(

        
        status = penzi_data.get("shortcode"),
        
    )

    penzi_m.save()
    serializer = UserSchema()
    penzi_data = serializer.dump(penzi_m)

    return jsonify(penzi_data), 201




@app.route("/recipe/<int:id>", methods = ["DELETE"])
def delete_recipe(id):
    recipe_to_delete = User.get_by_id(id)

    recipe_to_delete.delete()

    return jsonify({"message":"Deleted"}), 204
    

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Resource not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message": "Problem at local server"}), 500

if __name__ == "__main__":
    db.create_all()
    app.run(port=8001, debug=True)