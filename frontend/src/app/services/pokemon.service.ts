import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Pokemon, PokemonListResponse, Generation } from '../interfaces/pokemon.interface';

@Injectable({
  providedIn: 'root',
})
export class PokemonService {
  private http = inject(HttpClient);
  private apiUrl = 'http://192.168.3.182:5000/api/pokemon';

  listarPokemons(
    geracao: string,
    limit: number = 20,
    nome: string = ''
  ): Observable<PokemonListResponse> {
    let params = new HttpParams().set('geracao', geracao).set('limit', limit.toString());

    if (nome) {
      params = params.set('nome', nome);
    }

    return this.http.get<PokemonListResponse>(this.apiUrl, { params });
  }

  listarGeracoes(): Observable<{ geracoes: Generation[] }> {
    return this.http.get<{ geracoes: Generation[] }>(`${this.apiUrl}/geracoes`);
  }

  adicionarFavorito(pokemonId: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${pokemonId}/favorito`, {});
  }

  removerFavorito(pokemonId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${pokemonId}/favorito`);
  }

  adicionarGrupoBatalha(pokemonId: number): Observable<any> {
    return this.http.put(`${this.apiUrl}/${pokemonId}/grupo-batalha`, {});
  }

  removerGrupoBatalha(pokemonId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${pokemonId}/grupo-batalha`);
  }

  listarFavoritos(): Observable<{ favoritos: any[] }> {
    return this.http.get<{ favoritos: any[] }>(`${this.apiUrl}/favoritos`);
  }

  listarGrupoBatalha(): Observable<{ grupo_batalha: any[] }> {
    return this.http.get<{ grupo_batalha: any[] }>(`${this.apiUrl}/grupo-batalha`);
  }
}
