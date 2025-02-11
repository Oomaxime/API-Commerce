from flask import Flask, render_template, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'web2'
jwt = JWTManager(app)

users = [
    {"id": 1, "username": "admin", "password": "admin"}
]


@app.route('/connexion', methods=['POST'])
def connexion():
    username = request.form['username']
    password = request.form['password']

    for user in users:
        if user['username'] == username and user['password'] == password:
            access_token = create_access_token(identity=username)
            print(access_token)
            response = make_response(render_template('index.html'))
            response.set_cookie('access_token', access_token)
            return response
        else:
            return "Invalid credentials"

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form['firstname']
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    user = {"id": len(users) + 1, "firstname": firstname, "name": name, "username": username, "password": password, "email": email}
    users.append(user)

    return "User added successfully" + str(users)

@app.route('/signin')
def signin():
   return render_template('signin.html')


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/app')
@jwt_required()
def app():
    return render_template('app.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)