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
        nome = request.args.get('nome', '')
        geracao = request.args.get('geracao', '')
        
        if not geracao:
            return jsonify({'error': 'Parâmetro "geracao" é obrigatório'}), 400
                
        dados_geracao = PokeAPIService.obter_geracao(geracao)
        
        if not dados_geracao:
            return jsonify({'error': 'Geração não encontrada'}), 404
        
        pokemons_processados = []
        
        for especie in dados_geracao['pokemon_species']:
            if len(pokemons_processados) >= limite:
                break
                
            pokemon_id = especie['url'].split('/')[-2]
            
            dados_pokemon = PokeAPIService.obter_pokemon(pokemon_id)
            
            if not dados_pokemon:
                continue
            
            if nome and nome.lower() not in dados_pokemon['name'].lower():
                continue
            
            pokemon_usuario = PokemonUsuario.query.filter_by(
                IDUsuario=usuario_id, 
                Codigo=str(pokemon_id)
            ).first()
            
            pokemon_info = {
                'id': dados_pokemon['id'],
                'nome': dados_pokemon['name'],
                'imagem': dados_pokemon['sprites']['front_default'],
                'tipos': [tipo['type']['name'] for tipo in dados_pokemon['types']],
                'favorito': pokemon_usuario.Favorito if pokemon_usuario else False,
                'grupo_batalha': pokemon_usuario.GrupoBatalha if pokemon_usuario else False,
                'stats': dados_pokemon['stats'],
            }
            
            pokemons_processados.append(pokemon_info)
        
        return jsonify({
            'pokemons': pokemons_processados,
            'total': len(pokemons_processados),
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'})   , 500

@pokemon_bp.route('/favoritos', methods=['GET'])
@jwt_required()
def listar_favoritos():
    """GET /api/pokemon/favoritos - Listar favoritos do usuário"""
    try:
        usuario_id = get_jwt_identity()
        
        favoritos = PokemonUsuario.query.filter_by(
            IDUsuario=usuario_id,
            Favorito=True
        ).all()
        
        return jsonify({
            'favoritos': [pokemon.to_dict() for pokemon in favoritos]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@pokemon_bp.route('/<string:pokemon_id>/favorito', methods=['PUT', 'DELETE'])
@jwt_required()
def gerenciar_favorito(pokemon_id):
    """PUT/DELETE /api/pokemon/{id}/favorito - Gerenciar favorito"""
    try:
        usuario_id = get_jwt_identity()
        
        detalhes_pokemon = PokeAPIService.obter_pokemon(pokemon_id)
        if not detalhes_pokemon:
            return jsonify({'error': 'Pokémon não encontrado'}), 404
        
        pokemon_usuario = PokemonUsuario.query.filter_by(
            IDUsuario=usuario_id,
            Codigo=str(pokemon_id)
        ).first()
        
        if request.method == 'PUT':
            if not pokemon_usuario:
                tipos = PokeAPIService.processar_tipos_pokemon(detalhes_pokemon['types'])
                pokemon_usuario = PokemonUsuario(
                    IDUsuario=usuario_id,
                    Codigo=str(pokemon_id),
                    ImagemUrl=detalhes_pokemon['sprites']['front_default'],
                    Nome=detalhes_pokemon['name'],
                    Favorito=True,
                    GrupoBatalha=False
                )
                pokemon_usuario.adicionar_tipos(tipos)
                db.session.add(pokemon_usuario)
            else:
                pokemon_usuario.Favorito = True
            
            db.session.commit()
            return jsonify({'message': 'Pokémon adicionado aos favoritos'}), 200
        
        elif request.method == 'DELETE':
            if pokemon_usuario:
                pokemon_usuario.Favorito = False
                db.session.commit()
                return jsonify({'message': 'Pokémon removido dos favoritos'}), 200
            else:
                return jsonify({'error': 'Pokémon não encontrado nos favoritos'}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

@pokemon_bp.route('/grupo-batalha', methods=['GET'])
@jwt_required()
def listar_grupo_batalha():
    """GET /api/pokemon/grupo-batalha - Listar grupo de batalha"""
    try:
        usuario_id = get_jwt_identity()
        
        grupo_batalha = PokemonUsuario.query.filter_by(
            IDUsuario=usuario_id,
            GrupoBatalha=True
        ).all()
        
        return jsonify({
            'grupo_batalha': [pokemon.to_dict() for pokemon in grupo_batalha],
            'total': len(grupo_batalha),
            'maximo': 6
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

@pokemon_bp.route('/<string:pokemon_id>/grupo-batalha', methods=['PUT', 'DELETE'])
@jwt_required()
def gerenciar_grupo_batalha(pokemon_id):
    """PUT/DELETE /api/pokemon/{id}/grupo-batalha - Gerenciar grupo"""
    try:
        usuario_id = get_jwt_identity()
        
        if request.method == 'PUT':
            grupo_atual = PokemonUsuario.query.filter_by(
                IDUsuario=usuario_id,
                GrupoBatalha=True
            ).count()
            
            if grupo_atual >= 6:
                return jsonify({'error': 'Máximo de 6 Pokémon no grupo de batalha'}), 400
        
        detalhes_pokemon = PokeAPIService.obter_pokemon(pokemon_id)
        if not detalhes_pokemon:
            return jsonify({'error': 'Pokémon não encontrado'}), 404
        
        pokemon_usuario = PokemonUsuario.query.filter_by(
            IDUsuario=usuario_id,
            Codigo=str(pokemon_id)
        ).first()
        
        if request.method == 'PUT':
            if not pokemon_usuario:
                tipos = PokeAPIService.processar_tipos_pokemon(detalhes_pokemon['types'])
                pokemon_usuario = PokemonUsuario(
                    IDUsuario=usuario_id,
                    Codigo=str(pokemon_id),
                    ImagemUrl=detalhes_pokemon['sprites']['front_default'],
                    Nome=detalhes_pokemon['name'],
                    Favorito=False,
                    GrupoBatalha=True
                )
                pokemon_usuario.adicionar_tipos(tipos)
                db.session.add(pokemon_usuario)
            else:
                pokemon_usuario.GrupoBatalha = True
            
            db.session.commit()
            return jsonify({'message': 'Pokémon adicionado ao grupo de batalha'}), 200
        
        elif request.method == 'DELETE':
            if pokemon_usuario:
                pokemon_usuario.GrupoBatalha = False
                db.session.commit()
                return jsonify({'message': 'Pokémon removido do grupo de batalha'}), 200
            else:
                return jsonify({'error': 'Pokémon não encontrado no grupo'}), 404
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500
