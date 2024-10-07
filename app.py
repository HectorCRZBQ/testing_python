from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la base de datos
class Starfish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    limbs = db.Column(db.Integer, nullable=False)
    depth = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    latin_name = db.Column(db.String(80), nullable=False)
    habitat = db.Column(db.String(120), nullable=False)  # Atributo adicional

# Inicializar la base de datos
with app.app_context():
    db.create_all()

# Ruta principal: lista de estrellas de mar
@app.route('/')
def index():
    starfish_list = Starfish.query.all()
    return render_template('index.html', starfish_list=starfish_list)

# Ruta para crear una nueva estrella de mar (formulario)
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        color = request.form['color']
        limbs = request.form['limbs']
        depth = request.form['depth']
        age = request.form['age']
        gender = request.form['gender']
        latin_name = request.form['latin_name']
        habitat = request.form['habitat']

        new_starfish = Starfish(
            name=name,
            color=color,
            limbs=int(limbs),
            depth=float(depth),
            age=int(age),
            gender=gender,
            latin_name=latin_name,
            habitat=habitat
        )
        db.session.add(new_starfish)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# Ruta para actualizar una estrella de mar
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    starfish = Starfish.query.get_or_404(id)
    if request.method == 'POST':
        starfish.name = request.form['name']
        starfish.color = request.form['color']
        starfish.limbs = request.form['limbs']
        starfish.depth = request.form['depth']
        starfish.age = request.form['age']
        starfish.gender = request.form['gender']
        starfish.latin_name = request.form['latin_name']
        starfish.habitat = request.form['habitat']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', starfish=starfish)

# Ruta para eliminar una estrella de mar
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    starfish = Starfish.query.get_or_404(id)
    db.session.delete(starfish)
    db.session.commit()
    return redirect(url_for('index'))

# API para obtener todas las estrellas de mar (opcional, para usar con AJAX o pruebas)
@app.route('/api/starfish', methods=['GET'])
def get_starfish():
    starfish = Starfish.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'color': s.color,
        'limbs': s.limbs,
        'depth': s.depth,
        'age': s.age,
        'gender': s.gender,
        'latin_name': s.latin_name,
        'habitat': s.habitat
    } for s in starfish])

if __name__ == '__main__':
    app.run(debug=True)
