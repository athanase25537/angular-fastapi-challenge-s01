import { Component, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LinkComponent } from '../../aside/link/link-component/link-component';
import { LinkModel } from '../../aside/link/link-model';
import { faHome, faList, faCog } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-dashboard-component',
  standalone: true,
  imports: [CommonModule, LinkComponent],
  templateUrl: './dashboard-component.html',
  changeDetection: ChangeDetectionStrategy.Default,
})
export class DashboardComponent {
  links: LinkModel[] = [
    new LinkModel(faHome, 'Accueil', '/'),
    new LinkModel(faList, 'Mes items', '/items'),
    new LinkModel(faCog, 'Paramètres', '/settings'),
  ];
}
