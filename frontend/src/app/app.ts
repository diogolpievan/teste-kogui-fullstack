import { Component, signal } from '@angular/core';
import { Router, RouterOutlet, RouterModule } from '@angular/router'; // ✅ Adicionar RouterModule
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterModule], // ✅ Adicionar RouterModule aqui
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class AppComponent {
  protected readonly title = signal('Pokédex Kogui');

  constructor(private authService: AuthService, private router: Router) {}

  showHeader(): boolean {
    return this.authService.isAuthenticated();
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  getCurrentUser() {
    return this.authService.getCurrentUser();
  }

  goToHome(): void {
    this.router.navigate(['/home']);
  }

  goToFavorites(): void {
    this.router.navigate(['/favoritos']);
  }

  goToBattleTeam(): void {
    this.router.navigate(['/grupo-batalha']);
  }
}
