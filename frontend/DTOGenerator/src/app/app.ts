import { Component, signal } from '@angular/core';
import { AsideComponent } from "./aside/aside-component/aside-component";
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [AsideComponent, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('DTOGenerator');
}
