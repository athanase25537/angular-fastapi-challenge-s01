import { Component, ChangeDetectionStrategy, inject, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../core/auth/auth.service';
import { UserService } from '../core/users/user.service';
import type { UserRead } from '../core/api/generated';

@Component({ selector: 'app-profile', imports: [DatePipe, ReactiveFormsModule], templateUrl: './profile.component.html', styleUrl: './profile.component.css', changeDetection: ChangeDetectionStrategy.OnPush })
export class ProfileComponent {
  readonly auth = inject(AuthService); private readonly usersApi = inject(UserService); private readonly fb = inject(FormBuilder); private readonly router = inject(Router);
  readonly profile = signal<UserRead | null>(this.auth.user()); readonly loading = signal(false); readonly saving = signal(false); readonly editing = signal(false); readonly error = signal(''); readonly notice = signal('');
  readonly form = this.fb.nonNullable.group({ first_name: ['', Validators.required], last_name: ['', Validators.required], email: ['', [Validators.required, Validators.email]], phone_number: ['', Validators.required], date_of_birth: [''] });
  constructor() { this.load(); }

  load(): void {
    const user = this.auth.user(); if (!user) return; this.loading.set(true); this.error.set('');
    this.usersApi.get(user.id).subscribe({
      next: (response) => { const profile = response.data ?? user; this.setProfile(profile); this.loading.set(false); },
      error: (response) => { this.error.set(this.message(response, 'Unable to load profile.')); this.loading.set(false); },
    });
  }
  refresh(): void {
    this.loading.set(true); this.error.set('');
    this.auth.refreshProfile().subscribe({ next: (user) => { this.setProfile(user); this.loading.set(false); }, error: (response) => { this.error.set(this.message(response, 'Unable to refresh profile.')); this.loading.set(false); } });
  }
  beginEdit(): void { const user = this.profile(); if (!user) return; this.form.reset({ first_name: user.first_name, last_name: user.last_name, email: user.email, phone_number: user.phone_number, date_of_birth: user.date_of_birth ?? '' }); this.editing.set(true); this.notice.set(''); }
  save(): void {
    const user = this.profile(); if (!user || this.form.invalid || this.saving()) { this.form.markAllAsTouched(); return; } this.saving.set(true); this.error.set(''); const value = this.form.getRawValue();
    this.usersApi.update(user.id, { ...value, date_of_birth: value.date_of_birth || null }).subscribe({ next: (response) => { this.saving.set(false); this.editing.set(false); if (response.data) this.setProfile(response.data); this.notice.set(response.message); }, error: (response) => { this.saving.set(false); this.error.set(this.message(response, 'Unable to save your profile.')); } });
  }
  deleteAccount(): void {
    const user = this.profile(); if (!user || !confirm('Delete your account permanently? This action cannot be reversed.')) return; this.saving.set(true);
    this.usersApi.delete(user.id).subscribe({ next: () => { this.auth.logout(); void this.router.navigateByUrl('/register'); }, error: (response) => { this.saving.set(false); this.error.set(this.message(response, 'Unable to delete your account.')); } });
  }
  private setProfile(user: UserRead): void { this.profile.set(user); this.auth.persistUser(user); }
  private message(response: any, fallback: string): string { return response.error?.detail ?? fallback; }
}
