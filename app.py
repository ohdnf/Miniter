from flask import Flask, request, jsonify

app = Flask(__name__)
app.id_count = 1
app.users = {}

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user                = request.json
    new_user["id"]          = app.id_count
    app.users[app.id_count] = new_user
    app.id_count            = app.id_count + 1

    return jsonify(new_user)

app.tweets = []

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json
    user_id = int(payload['id'])
    tweet   = payload

    if user_id not in app.users:
        return 'User does not exist', 400

    elif len(tweet) > 300:
        return 'Exceeded 300 characters', 400

    else:
        app.tweets.append({
            'user_id' : user_id,
            'tweet'   : tweet
        })

        return '', 200

@app.route('/follow', methods=['POST'])
def follow():
    payload   = request.json
    user_id   = int(payload['id'])
    id2follow = int(payload['follow'])

    if user_id not in app.users or id2follow not in app.users:
        return 'User does not exist', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(id2follow)

@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload     = request.json
    user_id     = int(payload['id'])
    id2unfollow = int(payload['unfollow'])

    if user_id not in app.users or id2unfollow not in app.users:
        return 'User does not exist', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(id2unfollow)

from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)

        return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder

@app.route('/timeline/<int:user_id>'. methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return 'User does not exist', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id': user_id,
        'timeline': timeline
    })
