import { Component } from '@angular/core';
import { LinkComponent } from "../link/link-component/link-component";
import { LinkModel } from '../link/linkModel';

@Component({
  selector: 'app-aside-component',
  imports: [LinkComponent],
  templateUrl: './aside-component.html',
  styleUrl: './aside-component.css',
})
export class AsideComponent {
  link: LinkModel = {icon: "", title: "Dashboard", path: "/dashboard"};
}
