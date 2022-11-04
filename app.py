from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from datetime import datetime

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vasurupa0.db'

db = SQLAlchemy(app)

migrate = Migrate(app, db)


# Models
class Profile(db.Model):
    emp_code = db.Column(db.Integer, primary_key=True, nullable=False)
    emp_name = db.Column(db.String(20), nullable=True)
    dob = db.Column(db.String(20), nullable=True)
    doj = db.Column(db.String(20), nullable=True)
    doa = db.Column(db.String(20), nullable=True)
    # dob = db.Column(db.DateTime)
    # doj = db.Column(db.DateTime)
    # doa = db.Column(db.DateTime)
    email = db.Column(db.String(50), nullable=False)



    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Emp Code : {self.emp_code}, Name: {self.emp_name}, DoB: {self.dob}, DoJ: {self.doj}, DoA: {self.doa}"
        f"Email: {self.email}"


# function to render index page
@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')


# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    emp_code = request.form.get("emp_code")
    emp_name = request.form.get("emp_name")
    dob = request.form.get("dob")
    doj = request.form.get("doj")
    doa = request.form.get("doa")
    email = request.form.get("email")

    if emp_code != '' and emp_name != '' and dob != '' and doj != '' and doa != '' and email is not None:
        p = Profile(emp_code=emp_code, emp_name=emp_name, dob=dob, doj=doj, doa=doa, email=email)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


@app.route('/delete/<int:emp_code>')
def erase(emp_code):
    data = Profile.query.get(emp_code)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route('/edit/<int:emp_code>/update', methods=['GET', 'PUT','POST'])
def update(emp_code):
    data = Profile.query.filter_by(emp_code=emp_code).first()
    print(request.method)
    if request.method == 'POST':

        if data:
            data.emp_code = request.form.get("emp_code")
            data.emp_name = request.form.get("emp_name")
            data.dob = request.form.get("dob")
            data.doj = request.form.get("doj")
            data.doa = request.form.get("doa")
            data.email = request.form.get("email")
            db.session.commit()
            return redirect(f'/')
        return f"PROFILE with id = {emp_code} Does not exist"

    return render_template('edit.html', data=data)


# @app.route('/wish_table')
# def Wish():
#     return render_template('wish_table.html')


@app.route('/wish_table', methods=['GET', 'POST'])
def Date():
    all = Profile.query.all()
    today_date = datetime.today().date()

    # birthdays = Profile.queries.filter(dob.day=today_date.day, dob.month=today_date.month)
    # joining = Emp.objects.filter(DOJoining__day=today_date.day, DOJoining__month=today_date.month)
    # annversary = Emp.objects.filter(DOAnniversary__day=today_date.day, DOAnniversary__month=today_date.month)
    # return render(request, 'data.html', {'birthdays': birthdays, 'joining': joining, 'annversary': annversary})

    for i in all:
        birthday = datetime.strptime(i.dob, '%Y-%m-%d')
        joining = datetime.strptime(i.doj, '%Y-%m-%d')
        anniversary = datetime.strptime(i.doa, '%Y-%m-%d')
        Bday = ((birthday.day == today_date.day) and (birthday.month == today_date.month))
        if Bday:
            bday_obj = Profile.query.filter(Profile.emp_code == i.emp_code)

        Jday = ((joining.day == today_date.day) and (joining.month == today_date.month))
        if Jday:
            jday_obj = Profile.query.filter(Profile.emp_code == i.emp_code)

        Aday = ((anniversary.day == today_date.day) and (anniversary.month == today_date.month))
        if Aday:
            Aday_obj = Profile.query.filter(Profile.emp_code == i.emp_code)

    # if bday_obj and jday_obj and Aday_obj:

            return render_template('wish_table.html', bday_obj=bday_obj, jday_obj=jday_obj, Aday_obj=Aday_obj)
    return render_template('wish_table.html', bday_obj='', jday_obj='', Aday_obj='')


@app.route('/email')
def Email():
    return render_template('email.html')


if __name__ == '__main__':
    app.run(debug=True)
