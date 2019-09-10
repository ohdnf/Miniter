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