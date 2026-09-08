import { Component, ChangeDetectionStrategy, inject } from '@angular/core';
import { LinkComponent } from "../link/link-component/link-component";
import { LinkModel } from '../link/link-model';
import { faGear, faHome, faMoneyBill, faPuzzlePiece } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
@Component({
  selector: 'app-aside-component',
  imports: [LinkComponent, FontAwesomeModule],
  templateUrl: './aside-component.html',
  changeDetection: ChangeDetectionStrategy.Eager,
  styleUrl: './aside-component.css',
})
export class AsideComponent {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  
  myLinks: LinkModel[] = [
    {icon: faHome, title: "Dashboard", path: "/dashboard"},
    {icon: faMoneyBill, title: "Transactions", path: "/transactions"},
    {icon: faPuzzlePiece, title: "My profile", path: "/profile"},
    {icon: faGear, title: "Settings", path: "/profile"},
  ];

  logout(): void {
    this.auth.logout();
    void this.router.navigateByUrl('/login');
  }
}
