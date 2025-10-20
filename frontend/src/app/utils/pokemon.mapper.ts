import { Pokemon, PokemonUsuario, TipoPokemon } from '../interfaces/pokemon.interface';

export class PokemonMapper {
  static toPokemonUsuario(pokemon: Pokemon, usuarioId: number): PokemonUsuario {
    return {
      IDPokemonUsuario: 0,
      IDUsuario: usuarioId,
      Codigo: pokemon.id.toString(),
      ImagemUrl: pokemon.imagem,
      Nome: pokemon.nome,
      GrupoBatalha: pokemon.grupo_batalha,
      Favorito: pokemon.favorito,
      Tipos: pokemon.tipos.map((tipo) => ({
        IDTipoPokemon: 0,
        Descricao: tipo,
      })),
    };
  }

  static toPokemon(pokemonUsuario: PokemonUsuario): Pokemon {
    return {
      id: parseInt(pokemonUsuario.Codigo),
      nome: pokemonUsuario.Nome,
      imagem: pokemonUsuario.ImagemUrl,
      tipos: pokemonUsuario.Tipos.map((tipo) => tipo.Descricao),
      favorito: pokemonUsuario.Favorito,
      grupo_batalha: pokemonUsuario.GrupoBatalha,
    };
  }

  static toUniversalPokemon(data: Pokemon | PokemonUsuario): any {
    if ('id' in data) {
      return {
        id: data.id,
        nome: data.nome,
        imagem: data.imagem,
        tipos: data.tipos,
        favorito: data.favorito,
        grupo_batalha: data.grupo_batalha,
        Codigo: data.id.toString(),
        Nome: data.nome,
        ImagemUrl: data.imagem,
        Favorito: data.favorito,
        GrupoBatalha: data.grupo_batalha,
        Tipos: data.tipos.map((tipo) => ({ Descricao: tipo })),
      };
    } else {
      return {
        id: parseInt(data.Codigo),
        nome: data.Nome,
        imagem: data.ImagemUrl,
        tipos: data.Tipos.map((tipo) => tipo.Descricao),
        favorito: data.Favorito,
        grupo_batalha: data.GrupoBatalha,
        IDPokemonUsuario: data.IDPokemonUsuario,
        IDUsuario: data.IDUsuario,
        Codigo: data.Codigo,
        Nome: data.Nome,
        ImagemUrl: data.ImagemUrl,
        Favorito: data.Favorito,
        GrupoBatalha: data.GrupoBatalha,
        Tipos: data.Tipos,
      };
    }
  }
}
