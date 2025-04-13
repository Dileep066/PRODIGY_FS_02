from flask import Flask ,render_template, request, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///employee.db"
db=SQLAlchemy(app)
class Employee(db.Model):
    idnumber=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    role=db.Column(db.String(200))
    salary=db.Column(db.Float)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return {self.name}
with app.app_context():
    db.create_all()
@app.route('/employe',methods=['POST','GET'])
def employee():
    if request.method=='POST':
        idnumber=request.form['idnumber']
        name=request.form['Name']
        emp=Employee.query.filter_by(idnumber=idnumber).first()
        print(emp.name,name)
        if emp.name==name:
            return render_template('employe_one.html',emp=emp)
        else:
            return "ERRROR"
    return render_template('employe.html')

@app.route('/admin_login',methods=['POST','GET'])
def admin_login():
    if request.method=='POST':
        username=request.form['email']
        password=request.form['password']
        if username=='admin263@gmail.com' and password=="Dileep":
            return redirect('/admin')
    return render_template('admin_login.html')
@app.route('/admin',methods=['POST',"GET"])
def admin():
    if request.method=='POST':
        idnumber=request.form['idnumber']
        name=request.form['Name']
        role=request.form['Role']
        salary=request.form['salary']
        employe=Employee(idnumber=idnumber,name=name,role=role,salary=salary)
        db.session.add(employe)
        db.session.commit()
    allemployee=Employee.query.all()
    return render_template('admin.html',allemployee=allemployee)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/update/<int:idnumber>',methods=['POST','GET'])
def update(idnumber):
    if request.method=='POST':
        name = request.form['Name']
        role = request.form['Role']
        salary = request.form['salary']
        emp=Employee.query.filter_by(idnumber=idnumber).first()
        emp.name=name
        emp.role=role
        emp.salary=salary
        db.session.add(emp)
        db.session.commit()
        return redirect('/admin')
    emp=Employee.query.filter_by(idnumber=idnumber).first()
    return render_template('update.html',emp=emp)
@app.route('/delete/<int:idnumber>')
def delete(idnumber):
    emp=Employee.query.filter_by(idnumber=idnumber).first()
    db.session.delete(emp)
    db.session.commit()
    return redirect('/admin')
if __name__=="__main__":
    app.run(debug=True,port=8000)