from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

# EJEMPLO: renderizar a otra pagina
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

# EJEMPLO: leer valores
@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

if __name__ == "__main__":
    app.run()