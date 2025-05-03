from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)



class Todo(db.Model):
    sno= db.Column(db.Integer, primary_key = True)
    title= db.Column(db.String(200), nullable=False)
    desc= db.Column(db.String(500), nullable = False)
    date_created= db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title} -{self.desc}"


with app.app_context():
    db.create_all()
    
@app.route("/", methods =["POST","GET"])
def hello_world():
    if request.method == "POST":
        title=request.form["title"]
        desc=request.form["desc"]
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    all_todo=Todo.query.all()
    print(all_todo) 
    return render_template("index.html",all_todo=all_todo)

@app.route("/about_nav")
def about_nav():
    return redirect("index.html")

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:sno>",methods=["GET", "POST"])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == "POST":
        title = request.form.get("title")
        desc = request.form.get("desc")
        if title and desc:  # Basic validation
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
    return render_template("update.html",todo=todo)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "").strip()  # Fixed to use request.args
    if query:
        # Search todos where title or description contains the query (case-insensitive)
        all_todo = Todo.query.filter(
            (Todo.title.ilike(f"%{query}%")) | (Todo.desc.ilike(f"%{query}%"))
        ).all()
        print(all_todo)  # Kept for debugging
    else:
        all_todo = Todo.query.all()  # Show all todos if query is empty
    return render_template("index.html", all_todo=all_todo, query=query)

if __name__ == "__main__":
    app.run(debug=True)