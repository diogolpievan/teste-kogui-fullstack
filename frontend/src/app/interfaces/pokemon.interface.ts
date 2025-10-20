export interface Pokemon {
  id: number;
  nome: string;
  imagem: string;
  tipos: string[];
  favorito: boolean;
  grupo_batalha: boolean;
}

export interface PokemonListResponse {
  pokemons: Pokemon[];
  total: number;
  filtros: {
    nome: string;
    geracao: string;
    limit: number;
    offset: number;
  };
}

export interface Generation {
  id: string;
  nome: string;
}

export interface PokemonUsuario {
  IDPokemonUsuario: number;
  IDUsuario: number;
  Codigo: string;
  ImagemUrl: string;
  Nome: string;
  GrupoBatalha: boolean;
  Favorito: boolean;
  Tipos: TipoPokemon[];
}

export interface TipoPokemon {
  IDTipoPokemon: number;
  Descricao: string;
}
