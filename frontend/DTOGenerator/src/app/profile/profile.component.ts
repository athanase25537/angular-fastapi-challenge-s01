import { Component, ChangeDetectionStrategy, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { AuthService } from '../core/auth/auth.service';

@Component({
  selector: 'app-profile',
  imports: [DatePipe],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ProfileComponent {
  readonly auth = inject(AuthService);
  readonly loading = signal(false);
  readonly error = signal('');

  refresh(): void {
    this.loading.set(true); this.error.set('');
    this.auth.refreshProfile().subscribe({
      next: () => this.loading.set(false),
      error: (response) => { this.error.set(response.error?.detail ?? 'Unable to refresh profile.'); this.loading.set(false); },
    });
  }
}
