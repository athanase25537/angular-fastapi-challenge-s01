import { Component, ChangeDetectionStrategy } from '@angular/core';
import { LinkComponent } from "../link/link-component/link-component";
import { LinkModel } from '../link/link-model';
import { faGear, faHome, faMoneyBill, faPuzzlePiece } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
@Component({
  selector: 'app-aside-component',
  imports: [LinkComponent, FontAwesomeModule],
  templateUrl: './aside-component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './aside-component.css',
})
export class AsideComponent {
  
  myLinks: LinkModel[] = [
    {icon: faHome, title: "Dashboard", path: "/dashboard"},
    {icon: faMoneyBill, title: "Transactions", path: "/transactions"},
    {icon: faPuzzlePiece, title: "Modules", path: "/modules"},
    {icon: faGear, title: "Settings", path: "/settings"},
  ];
  
}
