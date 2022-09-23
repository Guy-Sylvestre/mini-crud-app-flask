
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create app flask
app = Flask(__name__)

# Configuration route database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create table
class Task(db.Model):
    '''Table Task'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.utcnow
        )

    def __repr__(self) -> str:
        '''return name'''
        return f"Todos : {self.name}"


@app.route("/", methods=["GET", "POST"])
def  index():
    '''Home page get default and post if user choose'''

    if request.method == "POST":
        '''Verifiez if le post de l'utilisateur est un POST'''
        name = request.form['name']
        new_task = Task(name=name)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Une erreur s'est produite"
    else:
        tasks = Task.query.order_by(Task.created_at)
        
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>/")
def delete(id):
    '''Delete name taks in reference your id'''

    task = Task.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "UNe erreurs s'est produite"


@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    '''Update a table task in refere your id'''
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        '''If suser request is POST'''
        task.name = request.form["name"]

        try:
            db.session.commit()
            return redirect("/")
        except Exception:
            return "Nous ne pouvons pas modifier la tache"
    else:
        '''If suser request isn't POST. But it's GET'''
        title = "Mise a jour"
        return render_template("update.html", title=title, task=task)

@app.route("/about/")
def  about():
    return render_template("about.html")


if __name__ == "_main__":
    app.run()