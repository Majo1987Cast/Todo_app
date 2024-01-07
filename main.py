#Libreria para el uso de flask
from flask import Flask, render_template, request, url_for, redirect

#Libreria para el uso de la base de dato
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


#Configuracion parametro "SQLALCHEMY_DATABASER_URI" con la ubicacion de la base de dato
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"

#Creacion de la base dato
db = SQLAlchemy(app)

#Ahora creamos la clase en este caso la orm

#Creamos la tabla de la base de dato
class Todo(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, nullable=False)
    state: Mapped[str] = mapped_column(db.String, nullable=False, default='Incompleto')

#Crea la base y tabla necesarias con el contexto de la aplicacion
with app.app_context():
    db.create_all()


#Creamos las rutas de la app
@app.route('/', methods=['GET', 'POST'])
def home():
    #SI SE DIO CLICK EN AGREGAR ES EL METODO POST
    if request.method == 'POST' :
      name = request.form.get('name')
      if name:
          obj = Todo(name=name)
          db.session.add(obj)
          db.session.commit()
          #return f'Agragado {name}'
    py_lista_tareas= Todo.query.all()
    return render_template('select.html', lista_tareas = py_lista_tareas)
    
@app.route('/update/<id>')
def update(id):
    obj =Todo.query.filter_by(id=id).first()
    obj.state = "Completo"
    db.session.commit()
    return redirect(url_for('home'))
    #return f'prueba para eliminar id {id}'

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/delete/<id>')
def delete(id):
    obj = Todo.query.filter_by(id=id).first()
    db.session.delete(obj)
    db.session.commit()
    return redirect(url_for('home'))


if __name__=='__main__':
    app.run(debug= True)