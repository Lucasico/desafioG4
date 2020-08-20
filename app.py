from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:28031998@127.0.0.1:5432/desafioG4"
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String)
    email = db.Column(db.String)
    endereco = db.Column(db.String)
    senha = db.Column(db.String)

    def __init__(self, nome, email, endereco, senha):
        self.nome = nome
        self.email = email
        self.endereco = endereco
        self.senha = senha

db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastroUsuario", methods=['GET','POST'])
def cadastroUsuario():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        endereco = request.form.get("endereco")
        senha = request.form.get("senha")

        if nome and email and endereco and senha:
            newUsuario = Usuario(nome, email, endereco, senha)
            db.session.add(newUsuario)
            db.session.commit()

        # redirecionando para a pagina de cadastro
    return redirect(url_for("index",cadastro="RealizadoComSucesso"))

@app.route("/listaUsuarios")
def listaUsuarios():
    usuarios = Usuario.query.order_by(Usuario._id).all()
    return render_template("listaUsuarios.html", usuarios=usuarios)

@app.route("/atualizarUsuario/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    usuario = Usuario.query.filter_by(_id=id).first()
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        endereco = request.form.get("endereco")
        senha = request.form.get("senha")

        if nome and email and endereco and senha:
            usuario.nome = nome
            usuario.email = email
            usuario.endereco = endereco
            usuario.senha = senha
            db.session.commit()
            return redirect(url_for("listaUsuarios"))
    return render_template("atualizarUsuario.html", usuario=usuario)

@app.route("/excluirUsuario/<int:id>")
def excluir(id):
    usuario = Usuario.query.filter_by(_id=id).first()
    db.session.delete(usuario)
    db.session.commit()

    usuario = usuario.query.all()
    return render_template("listaUsuarios.html", usuarios=usuario)

if __name__ =='__main__':
    app.run(debug=True)