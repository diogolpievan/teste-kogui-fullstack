import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { PokemonService } from '../../services/pokemon.service';
import { Pokemon, Generation } from '../../interfaces/pokemon.interface';

@Component({
  selector: 'app-pokemon-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './pokemon-list.html',
  styleUrl: './pokemon-list.css',
})
export class PokemonListComponent implements OnInit {
  pokemons = signal<Pokemon[]>([]);
  carregando = signal(false);
  erro = signal('');

  geracoes = signal<Generation[]>([
    { id: '1', nome: 'Geração 1 - Kanto' },
    { id: '2', nome: 'Geração 2 - Johto' },
    { id: '3', nome: 'Geração 3 - Hoenn' },
    { id: '4', nome: 'Geração 4 - Sinnoh' },
    { id: '5', nome: 'Geração 5 - Unova' },
    { id: '6', nome: 'Geração 6 - Kalos' },
    { id: '7', nome: 'Geração 7 - Alola' },
    { id: '8', nome: 'Geração 8 - Galar' },
    { id: '9', nome: 'Geração 9 - Paldea' },
  ]);

  geracaoSelecionada = signal('1');
  nomeFiltro = signal('');
  limite = signal(20);

  constructor(private pokemonService: PokemonService) {}

  ngOnInit(): void {
    this.carregarGeracoes();
    this.carregarPokemons();
  }

  carregarGeracoes(): void {
    this.pokemonService.listarGeracoes().subscribe({
      next: (response) => {
        this.geracoes.set(response.geracoes);
      },
      error: (error) => {
        console.error('Erro ao carregar gerações:', error);
      },
    });
  }

  carregarPokemons(): void {
    this.carregando.set(true);
    this.erro.set('');

    this.pokemonService
      .listarPokemons(this.geracaoSelecionada(), this.limite(), this.nomeFiltro())
      .subscribe({
        next: (response) => {
          this.pokemons.set(response.pokemons);
          this.carregando.set(false);
        },
        error: (error) => {
          this.erro.set('Erro ao carregar Pokémon');
          this.carregando.set(false);
          console.error('Erro:', error);
        },
      });
  }

  onGeracaoChange(geracao: string): void {
    this.geracaoSelecionada.set(geracao);
    this.carregarPokemons();
  }

  onNomeFiltroChange(nome: string): void {
    this.nomeFiltro.set(nome);
    setTimeout(() => {
      this.carregarPokemons();
    }, 500);
  }

  toggleFavorito(pokemon: Pokemon): void {
    const wasFavorite = pokemon.favorito;

    pokemon.favorito = !wasFavorite;

    const request = wasFavorite
      ? this.pokemonService.removerFavorito(pokemon.id)
      : this.pokemonService.adicionarFavorito(pokemon.id);

    request.subscribe({
      error: (error) => {
        pokemon.favorito = wasFavorite;
        console.error('Erro ao atualizar favorito:', error);
      },
    });
  }

  toggleGrupoBatalha(pokemon: Pokemon): void {
    const wasInBattleGroup = pokemon.grupo_batalha;

    pokemon.grupo_batalha = !wasInBattleGroup;

    const request = wasInBattleGroup
      ? this.pokemonService.removerGrupoBatalha(pokemon.id)
      : this.pokemonService.adicionarGrupoBatalha(pokemon.id);

    request.subscribe({
      error: (error) => {
        pokemon.grupo_batalha = wasInBattleGroup;
        console.error('Erro ao atualizar grupo de batalha:', error);
      },
    });
  }

  getTipoClass(tipo: string): string {
    return `tipo-${tipo.toLowerCase()}`;
  }
}
