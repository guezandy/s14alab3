from flask import Flask, render_template, request, redirect, url_for
from models.user import db, User
from modules.userform import UserForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sclpzykpoiiusc:c1305d2bab60b9a949c6b6a3514ecbf80fb2d2485065a76735717b6983cbf874@ec2-34-206-31-217.compute-1.amazonaws.com:5432/dif1elffb6b86' # 'postgresql://localhost/usersdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "s14a-key"
db.init_app(app)

@app.route('/')
def index():
    # Query all
    users = User.query.all()

    # Iterate and print
    for user in users:
        User.toString(user)

    return render_template("index.html", users=users)


@app.route('/adduser', methods=['GET', 'POST'])
def addUser():
    form = UserForm()
    # If GET
    if request.method == 'GET':
        return render_template('adduser.html', form=form)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            new_user = User(first_name=first_name, age=age)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form)


@app.route('/adduser/<first_name>/<age>')
def addUserFromUrl(first_name, age):
    db.session.add(User(first_name=first_name, age=age))
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/user/<user_id>')
def userDetails(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    return render_template('user.html', user=user)


@app.route('/deleteuser/<user_id>')
def deleteUser(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/updateuser/<user_id>', methods=['GET', 'POST'])
def updateUser(user_id):
    form = UserForm()
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return redirect(url_for('index'))
    # If GET
    if request.method == 'GET':
        user = User.query.filter_by(user_id=user_id).first()
        return render_template('adduser.html', form=form, user=user)
    # If POST
    else:
        if form.validate_on_submit():
            first_name = request.form['first_name']
            age = request.form['age']
            user.first_name = first_name
            user.age = age
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('adduser.html', form=form, user=user)

@app.route('/generatedata')
def generateData():
    for first_name, age in [
        ('Chris', 29),
        ('Michael', 27),
        ('Andrew', 27),
        ('Tony', 25),
        ('Ryan', 19),
    ]:
        db.session.add(User(first_name=first_name, age=age))
    db.session.commit()
    return redirect(url_for('index'))