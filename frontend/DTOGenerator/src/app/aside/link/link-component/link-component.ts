import { Component, input, ChangeDetectionStrategy } from '@angular/core';
import { LinkModel } from '../link-model';
import { RouterLink, RouterLinkActive } from "@angular/router";
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

@Component({
  selector: 'app-link-component',
  imports: [FontAwesomeModule, RouterLink, RouterLinkActive],
  templateUrl: './link-component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './link-component.css',
})
export class LinkComponent {
  myLink = input.required<LinkModel>();
}
