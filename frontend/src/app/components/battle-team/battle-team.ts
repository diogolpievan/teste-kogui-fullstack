import { Component, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { PokemonService } from '../../services/pokemon.service';
import { PokemonUsuario } from '../../interfaces/pokemon.interface';

@Component({
  selector: 'app-battle-team',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './battle-team.html',
  styleUrl: './battle-team.css',
})
export class BattleTeamComponent implements OnInit {
  grupoBatalha = signal<PokemonUsuario[]>([]);
  carregando = signal(true);
  erro = signal('');

  constructor(private pokemonService: PokemonService) {}

  ngOnInit(): void {
    this.carregarGrupoBatalha();
  }

  carregarGrupoBatalha(): void {
    this.carregando.set(true);
    this.erro.set('');

    this.pokemonService.listarGrupoBatalha().subscribe({
      next: (response) => {
        this.grupoBatalha.set(response.grupo_batalha || []);
        this.carregando.set(false);
      },
      error: (error) => {
        this.erro.set('Erro ao carregar grupo de batalha');
        this.carregando.set(false);
        console.error('Erro:', error);
      },
    });
  }

  removerDoGrupo(pokemon: PokemonUsuario): void {
    this.pokemonService.removerGrupoBatalha(parseInt(pokemon.Codigo)).subscribe({
      next: () => {
        this.grupoBatalha.set(
          this.grupoBatalha().filter((p) => p.IDPokemonUsuario !== pokemon.IDPokemonUsuario)
        );
      },
      error: (error) => {
        console.error('Erro ao remover do grupo:', error);
      },
    });
  }

  getTipoClass(tipo: string): string {
    return `tipo-${tipo.toLowerCase()}`;
  }

  calcularEstatisticasTime(): { total: number; max: number } {
    return {
      total: this.grupoBatalha().length,
      max: 6,
    };
  }
}
