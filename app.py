from flask import Flask ,request,redirect
from flask import  render_template 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager,login_user,UserMixin ,logout_user
from datetime import datetime

app = Flask(__name__)

# these for creating db

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydb.db"   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
from sqlalchemy import Integer, String
from sqlalchemy import Column
db = SQLAlchemy (app)
app.app_context().push()

app.config['SECRET_KEY']='thisissecret'

# these is for modals
class User( UserMixin ,db.Model):
     id = Column(Integer, primary_key=True)
     username = Column(String(50), unique=True)
     lastname = Column(String(50), unique=True)
     email = Column(String(120), unique=True)
     message= Column(String(50), unique=True)


class Bloger( UserMixin,db.Model):
     blog_id = db.Column(db.Integer, primary_key=True)
     tittle = db.Column(db.String(80),  nullable=False)
     author= db.Column(db.String(20), nullable=False)
     content = db.Column(db.Text() , nullable=False)
     pub_date = db.Column(db.DateTime() , nullable=False, default=datetime.now())



login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
 return User.query.get(int(user_id))


@app.route('/')
def hello_world():
    data=Bloger.query.all()
    return render_template ("index.html" ,data=data)


@app.route('/form', methods= ['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form['username']
        lastname= request.form['lastname']
        email = request.form['email']
        message = request.form['message']
        user = User(username=username,
                          lastname=lastname,
                          email=email,message=message)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")   
    return render_template ("form.html")


@app.route('/login',  methods = ['GET', 'POST'])
def login():

      if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user=User.query.filter_by(username=username).first()  
        if user and email==user.email:
            login_user(user)                                  
            return redirect ('/')
        else:
         return redirect ('/form')
        
      return render_template ("login.html")

@app.route('/blog', methods = ['GET', 'POST'])
def blog():
     if request.method == 'POST':
        tittle= request.form['tittle']
        author= request.form['author']
        content= request.form['content']
        blog= Bloger(tittle=tittle,
                          author=author,
                          content=content)
        db.session.add(blog)
        db.session.commit()
        return redirect('/')

     return render_template ("blog.html")


@app.route("/logout")
def logout():
   logout_user()
   return redirect ('/')
    
@app.route("/blogpage/<int:id>", methods = ['GET', 'POST'])
def blogpage(id):
   blog=Bloger.query.get(id)
   return render_template ("blogpage.html", blog=blog)

@app.route("/delet/<int:id>", methods = ['GET', 'POST'])
def delet(id):
   blog=Bloger.query.get(id)
   db.session.delete(blog)
   db.session.commit()

   return redirect ('/')

@app.route("/edit/<int:id>", methods = ['GET', 'POST'])
def edit(id):
   blog=Bloger.query.get(id)
   if request.method == 'POST':
        blog.tittle= request.form['tittle']
        blog.author= request.form['author']
        blog.content= request.form['content']
        db.session.commit()
        return redirect ('/')
   return render_template ("edit.html",blog=blog)




if __name__=="__main__":
    app.run(debug=True ,port=8000)