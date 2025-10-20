from app import db
from datetime import datetime

pokemon_tipos = db.Table('pokemon_tipos',
    db.Column('IDPokemonUsuario', db.Integer, db.ForeignKey('PokemonUsuario.IDPokemonUsuario'), primary_key=True),
    db.Column('IDTipoPokemon', db.Integer, db.ForeignKey('TipoPokemon.IDTipoPokemon'), primary_key=True),
    db.Column('Dtinclusao', db.DateTime, default=datetime.utcnow)
)

class PokemonUsuario(db.Model):
    __tablename__ = 'PokemonUsuario'
    
    IDPokemonUsuario = db.Column(db.Integer, primary_key=True)
    IDUsuario = db.Column(db.Integer, db.ForeignKey('Usuario.IDUsuario'), nullable=False)
    Codigo = db.Column(db.String(50), nullable=False)  # ID do Pokémon na PokeAPI
    ImagemUrl = db.Column(db.String(500))
    Nome = db.Column(db.String(100), nullable=False)
    GrupoBatalha = db.Column(db.Boolean, default=False)
    Favorito = db.Column(db.Boolean, default=False)
    
    tipos = db.relationship('TipoPokemon', 
                          secondary=pokemon_tipos,
                          lazy='subquery',
                          backref=db.backref('pokemons', lazy=True))
    
    def __init__(self, IDUsuario, Codigo, ImagemUrl, Nome, GrupoBatalha=False, Favorito=False):
        self.IDUsuario = IDUsuario
        self.Codigo = Codigo
        self.ImagemUrl = ImagemUrl
        self.Nome = Nome
        self.GrupoBatalha = GrupoBatalha
        self.Favorito = Favorito
    
    def adicionar_tipo(self, tipo):
        """Adicionar um tipo ao Pokémon"""
        if tipo not in self.tipos:
            self.tipos.append(tipo)
    
    def adicionar_tipos(self, lista_tipos):
        """Adicionar múltiplos tipos ao Pokémon"""
        for tipo in lista_tipos:
            self.adicionar_tipo(tipo)
    
    def to_dict(self):
        return {
            'IDPokemonUsuario': self.IDPokemonUsuario,
            'IDUsuario': self.IDUsuario,
            'Codigo': self.Codigo,
            'ImagemUrl': self.ImagemUrl,
            'Nome': self.Nome,
            'GrupoBatalha': self.GrupoBatalha,
            'Favorito': self.Favorito,
            'Tipos': [tipo.to_dict() for tipo in self.tipos]
        }
    
    def __repr__(self):
        return f'<PokemonUsuario {self.Nome}>'
