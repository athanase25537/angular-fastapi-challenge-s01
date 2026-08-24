import { Component, Input, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { LinkModel } from '../link-model';

@Component({
  selector: 'app-link-component',
  standalone: true,
  imports: [CommonModule, RouterModule, FontAwesomeModule],
  templateUrl: './link-component.html',
  changeDetection: ChangeDetectionStrategy.Default,
})
export class LinkComponent {
  @Input() myLink!: LinkModel;
}
