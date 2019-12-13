from flask import Flask, request, jsonify, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine, text


def create_app(test_config = None):
    app = Flask(__name__)
    #do.init_app(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    db = create_engine(app.config['DB_URL'], encoding = 'utf-8', max_overflow = 0)
    app.database = db

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user    = request.json
        new_user_id = app.database.execute(text("""
                    insert into users (
                        name,
                        email,
                        profile,
                        hashed_password
                    ) values (
                        :name,
                        :email,
                        :profile,
                        :password
                    )
                """), new_user).lastrowid
        row = current_app.database.execute(text("""
                    select
                        id,
                        name,
                        email,
                        profile
                    from users
                    where id = :user_id
                """), {
                    'user_id' : new_user_id
                }).fetchone()
        created_user = {
                'id' : row['id'],
                'name' : row['name'],
                'email' : row['email'],
                'profile' : row['profile']
            } if row else None

        return jsonify(created_user)
    
    return app
    


'''
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

@app.route('/timeline/<int:user_id>', methods=['GET'])
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
'''

