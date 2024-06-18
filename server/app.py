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

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = [message.to_dict() for message in Message.query.order_by('created_at').all()]

    if request.method == 'GET':
        msg_json = jsonify(messages)
        return msg_json
        

    elif request.method == 'POST':
        request_data = request.get_json()
        body = request_data.get('body')
        username = request_data.get('username')

        new_msg = Message(
            body = body,
            username = username,
        )

        db.session.add(new_msg)
        db.session.commit()

        msg_json = jsonify(new_msg.to_dict())
        return msg_json
    
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        request_data = request.get_json()
        new_body = request_data.get('body')

        if new_body is not None:
            message.body = new_body
            db.session.commit()

        return jsonify(message.to_dict())



    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

if __name__ == '__main__':
    app.run(port=5555)
