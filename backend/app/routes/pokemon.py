from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.pokemon_usuario import PokemonUsuario
from app.services.pokeapi_service import PokeAPIService
from app import db

pokemon_bp = Blueprint('pokemon', __name__)
@pokemon_bp.route('', methods=['GET'])
@jwt_required()
def listar_pokemons():
    try:
        usuario_id = get_jwt_identity()
        
        limite = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        nome = request.args.get('nome', '')
        geracao = request.args.get('geracao', '')
        
        # ✅ GERAÇÃO OBRIGATÓRIA
        if not geracao:
            return jsonify({'error': 'Parâmetro "geracao" é obrigatório'}), 400
        
        pokemons_processados = []
        contador = 0
        current_offset = offset
        
        while len(pokemons_processados) < limite: 
            dados_pokemons = PokeAPIService._fazer_requisicao(
                f"pokemon?limit={min(100, limite * 2)}&offset={current_offset}"
            )
            
            if not dados_pokemons or not dados_pokemons['results']:
                break
            
            for pokemon in dados_pokemons['results']:
                dados_pokemon = PokeAPIService.obter_pokemon(pokemon['name'])
                
                if not dados_pokemon:
                    continue
                
                dados_especie = PokeAPIService.obter_pokemon_especie(dados_pokemon['id'])
                
                if not dados_especie:
                    continue
                
                especie_geracao = dados_especie.get('generation', {}).get('name', '')
                if not especie_geracao or geracao not in especie_geracao:
                    continue
                
                if nome and nome.lower() not in dados_pokemon['name'].lower():
                    continue
                
                pokemon_usuario = PokemonUsuario.query.filter_by(
                    IDUsuario=usuario_id, 
                    Codigo=str(dados_pokemon['id'])
                ).first()
                
                pokemon_info = {
                    'id': dados_pokemon['id'],
                    'nome': dados_pokemon['name'],
                    'imagem': dados_pokemon['sprites']['front_default'],
                    'tipos': [tipo['type']['name'] for tipo in dados_pokemon['types']],
                    'favorito': pokemon_usuario.Favorito if pokemon_usuario else False,
                    'grupo_batalha': pokemon_usuario.GrupoBatalha if pokemon_usuario else False,
                    'geracao': especie_geracao
                }
                
                pokemons_processados.append(pokemon_info)
                
                if len(pokemons_processados) >= limite:
                    break
            
            current_offset += len(dados_pokemons['results'])
        
        return jsonify({
            'pokemons': pokemons_processados,
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500
