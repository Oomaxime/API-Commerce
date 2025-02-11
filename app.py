from flask import Flask, render_template, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'web2'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'admin' and password == 'admin':
        access_token = create_access_token(identity=username)
        response = make_response(render_template('index.html'))
        response.set_cookie('access_token', access_token)
        return response
    return "error"


@app.route('/')
def index():
    access_token = request.cookies.get('access_token')
    print(access_token)
    if access_token:
        return render_template('index.html')
    return render_template('login.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)