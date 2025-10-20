import requests

class PokeAPIService:
    BASE_URL = "https://pokeapi.co/api/v2"
    
    @classmethod
    def _fazer_requisicao(cls, endpoint):
        try:
            response = requests.get(f"{cls.BASE_URL}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro na requisição para {endpoint}: {e}")
            return None
    
    @classmethod
    def listar_geracoes(cls):
        return cls._fazer_requisicao("generation")
    
    @classmethod
    def obter_geracao(cls, geracao_id):
        return cls._fazer_requisicao(f"generation/{geracao_id}")
    
    @classmethod
    def obter_pokemon_especie(cls, especie_id):
        return cls._fazer_requisicao(f"pokemon-species/{especie_id}")
    
    @classmethod
    def obter_pokemon(cls, pokemon_id):
        return cls._fazer_requisicao(f"pokemon/{pokemon_id}")
    
    @classmethod
    def obter_geracao_pokemon(cls, pokemon_id):
        """Obter geração de um Pokémon através da espécie"""
        dados_especie = cls.obter_pokemon_especie(pokemon_id)
        
        if dados_especie and 'generation' in dados_especie:
            geracao_url = dados_especie['generation']['url']
            geracao_nome = geracao_url.split('/')[-2]
            return geracao_nome
        
        return None
    
    @classmethod
    def processar_tipos_pokemon(cls, tipos_data):
        from app.models.tipo_pokemon import TipoPokemon
        
        tipos = []
        for tipo_info in tipos_data:
            nome_tipo = tipo_info['type']['name'].title()
            tipo = TipoPokemon.obter_ou_criar(nome_tipo)
            tipos.append(tipo)
        
        return tipos
