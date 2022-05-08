from flask import Flask, jsonify, request

app = Flask(__name__)

client = app.test_client()


message = [
    {
        'id': 1,
        'text': 'Intro',
    },
    {
        'id': 2,
        'title': 'Video #2. More features',
        'description': 'PUT, DELETE routes'
    }
]


@app.route('/message', methods=['GET'])
def get_list():
    return jsonify(message)


@app.route('/message', methods=['POST'])
def update_list():
    new_one = request.json
    message.append(new_one)
    return jsonify(message)


@app.route('/message/<int:message_id>', methods=['PUT'])
def update_message(message_id):
    item = next((x for x in message if x['id'] == message_id), None)
    params = request.json
    if not item:
        return {'message': 'No message with this id'}, 400
    item.update(params)
    return item


@app.route('/message/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    idx, _ = next((x for x in enumerate(message)
                   if x[1]['id'] == message_id), (None, None))

    message.pop(idx)
    return '', 204


if __name__ == '__main__':
    app.run()

