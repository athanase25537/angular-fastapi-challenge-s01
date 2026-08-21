import { Component, input } from '@angular/core';
import { LinkModel } from '../linkModel';
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-link-component',
  imports: [RouterLink],
  templateUrl: './link-component.html',
  styleUrl: './link-component.css',
})
export class LinkComponent {
  myLink = input.required<LinkModel>();
}
