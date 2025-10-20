from app import db

class TipoPokemon(db.Model):
    __tablename__ = 'TipoPokemon'
    
    IDTipoPokemon = db.Column(db.Integer, primary_key=True)
    Descricao = db.Column(db.String(100), nullable=False, unique=True)
    
    def __init__(self, Descricao):
        self.Descricao = Descricao
    
    def to_dict(self):
        return {
            'IDTipoPokemon': self.IDTipoPokemon,
            'Descricao': self.Descricao
        }
    
    def __repr__(self):
        return f'<TipoPokemon {self.Descricao}>'
    
    @classmethod
    def obter_ou_criar(cls, descricao):
        tipo = cls.query.filter_by(Descricao=descricao).first()
        if not tipo:
            tipo = cls(Descricao=descricao)
            db.session.add(tipo)
            db.session.commit()
        return tipo
