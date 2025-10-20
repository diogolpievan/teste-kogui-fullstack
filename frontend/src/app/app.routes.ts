import { Routes } from '@angular/router';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () => import('./components/login/login').then((m) => m.LoginComponent),
  },
  {
    path: '',
    loadComponent: () =>
      import('./components/pokemon-list/pokemon-list').then((m) => m.PokemonListComponent),
    canActivate: [authGuard],
  },
  {
    path: 'pokemon',
    loadComponent: () =>
      import('./components/pokemon-list/pokemon-list').then((m) => m.PokemonListComponent),
    canActivate: [authGuard],
  },
  {
    path: 'favoritos',
    loadComponent: () =>
      import('./components/favorites/favorites').then((m) => m.FavoritesComponent),
    canActivate: [authGuard],
  },
  {
    path: 'grupo-batalha',
    loadComponent: () =>
      import('./components/battle-team/battle-team').then((m) => m.BattleTeamComponent),
    canActivate: [authGuard],
  },
  {
    path: '',
    redirectTo: '',
    pathMatch: 'full',
  },
  { path: '**', redirectTo: '' },
];
