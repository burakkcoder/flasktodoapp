from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/393974/Desktop/Python Kodlama Egzersizleri-VSCode/17 - Flask ,ORM ve SqlAlchemy ile Todo App/todo.db'
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html",todos = todos)

@app.route("/add",methods = ["POST"])
def addTodo():
    title = request.form.get("title") #title ismi formun içine gitti. oraya da yazdık..
    newTodo = Todo(title = title,complete = False) # title ı title olacak ve complete yani yapıp yapmadığı False ile başlayacak.
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo = Todo.query.filter_by(id = id).first() # id ye göre filter yapıcak ve o id nin ilkini alıcak kiii, zaten o id den bir tane var.
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete # yukarıdaki if işleminin daha kısa halini yapmış olduk burada.

    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("index"))

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean) # burada true yada false olcağı için böyle yazdık.

if __name__ == "__main__":
    db.create_all()  # Bu bir seferliğine çalışacak. tabloyu oluşturacak.
    app.run(debug=True)