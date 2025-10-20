from datetime import datetime
from extensions import db, bcrypt

class Usuario(db.Model):
    __tablename__ = "usuarios"

    IDUsuario = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(150), nullable=False)
    Login = db.Column(db.String(100), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Senha = db.Column(db.String(128), nullable=False)
    DtInclusao = db.Column(db.DateTime, default=datetime.now())
    DtAlteracao = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def set_password(self, password):
        self.Senha = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.Senha, password)

    def to_dict(self):
        return {
            "IDUsuario": self.IDUsuario,
            "Nome": self.Nome,
            "Login": self.Login,
            "Email": self.Email,
            "DtInclusao": self.DtInclusao.isoformat(),
            "DtAlteracao": self.DtAlteracao.isoformat(),
        }
