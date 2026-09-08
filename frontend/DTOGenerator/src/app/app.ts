import { Component, signal, ChangeDetectionStrategy, inject } from '@angular/core';
import { AsideComponent } from "./aside/aside-component/aside-component";
import { RouterOutlet } from '@angular/router';
import { AuthService } from './core/auth/auth.service';

@Component({
  selector: 'app-root',
  imports: [AsideComponent, RouterOutlet],
  templateUrl: './app.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './app.css'
})
export class App {
  readonly auth = inject(AuthService);
  protected readonly title = signal('DTOGenerator');
}
