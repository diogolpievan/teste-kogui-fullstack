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
