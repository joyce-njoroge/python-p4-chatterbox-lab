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

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.all()
    message_list = []
    for message in messages:
        message_data = {
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        }
        message_list.append(message_data)
    return jsonify(message_list)


@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if message:
        data = request.get_json()
        message.body = data.get('body', message.body)
        db.session.commit()
        return jsonify({
            'id': message.id,
            'body': message.body,
            'username': message.username,
            'created_at': message.created_at,
            'updated_at': message.updated_at
        })
    else:
        return jsonify({'error': 'Message not found'}), 404

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return '', 204  # Return 204 No Content for successful deletion
    else:
        return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(port=5555)
