import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { PokemonService } from '../../services/pokemon.service';
import { PokemonUsuario } from '../../interfaces/pokemon.interface';

@Component({
  selector: 'app-favorites',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './favorites.html',
  styleUrl: './favorites.css',
})
export class FavoritesComponent implements OnInit {
  favoritos = signal<PokemonUsuario[]>([]);
  carregando = signal(true);
  erro = signal('');

  constructor(private pokemonService: PokemonService) {}

  ngOnInit(): void {
    this.carregarFavoritos();
  }

  carregarFavoritos(): void {
    this.carregando.set(true);
    this.erro.set('');

    this.pokemonService.listarFavoritos().subscribe({
      next: (response) => {
        this.favoritos.set(response.favoritos || []);
        this.carregando.set(false);
      },
      error: (error) => {
        this.erro.set('Erro ao carregar favoritos');
        this.carregando.set(false);
        console.error('Erro:', error);
      },
    });
  }

  removerFavorito(pokemon: PokemonUsuario): void {
    this.pokemonService.removerFavorito(parseInt(pokemon.Codigo)).subscribe({
      next: () => {
        // Remove da lista local
        this.favoritos.set(
          this.favoritos().filter((p) => p.IDPokemonUsuario !== pokemon.IDPokemonUsuario)
        );
      },
      error: (error) => {
        console.error('Erro ao remover favorito:', error);
      },
    });
  }

  adicionarGrupoBatalha(pokemon: PokemonUsuario): void {
    this.pokemonService.adicionarGrupoBatalha(parseInt(pokemon.Codigo)).subscribe({
      next: () => {
        const updated = this.favoritos().map((p) =>
          p.IDPokemonUsuario === pokemon.IDPokemonUsuario ? { ...p, GrupoBatalha: true } : p
        );
        this.favoritos.set(updated);
      },
      error: (error) => {
        console.error('Erro ao adicionar ao grupo:', error);
      },
    });
  }

  getTipoClass(tipo: string): string {
    return `tipo-${tipo.toLowerCase()}`;
  }
}
