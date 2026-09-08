import { Component, ChangeDetectionStrategy, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-dashboard-component',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './dashboard-component.html',
  changeDetection: ChangeDetectionStrategy.Default,
})
export class DashboardComponent {
  readonly auth = inject(AuthService);
}
