from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.to_dict() for message in messages])

@app.post('/messages')
def post_a_message():
    data = request.json
    try:
        new_message = Message(body=data["body"], username=data["username"])
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message.to_dict()), 201
    except Exception as exception:
        return jsonify({"error":str(exception)}), 400

@app.patch('/messages/<int:id>')
def update_message(id):
    data = request.json
    message = db.session.get(Message,id)
    if message:
        try:
            for key in data:
                setattr(message, key, data[key])
            db.session.add(message)
            db.session.commit()
            return jsonify(message.to_dict()),200
        except Exception as exception:
            return jsonify({"error": str(exception)}), 400
    else:
        return jsonify({"error":"Message id not found."}), 404
    
@app.delete('/messages/<int:id>')
def delete_message(id):
    message = db.session.get(Message, id)
    if message:
        try: 
            db.session.delete(message)
            db.session.commit()
            return jsonify({}), 204
        except Exception as exception: 
            return jsonify({"error":str(exception)}), 400
    else: 
        return jsonify({"error": "Message ID not found"})

if __name__ == '__main__':
    app.run(port=5555)
