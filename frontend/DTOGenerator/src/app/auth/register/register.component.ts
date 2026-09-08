import { Component, ChangeDetectionStrategy, inject, signal } from '@angular/core';
import { ReactiveFormsModule, Validators, FormBuilder } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './register.component.html',
  styleUrl: '../login/auth-page.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RegisterComponent {
  private readonly fb = inject(FormBuilder);
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  readonly loading = signal(false);
  readonly error = signal('');
  readonly form = this.fb.nonNullable.group({
    first_name: ['', Validators.required], last_name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]], phone_number: ['', Validators.required],
    date_of_birth: [''], password: ['', [Validators.required, Validators.minLength(8)]],
    confirmPassword: ['', Validators.required],
  });

  submit(): void {
    if (this.form.invalid || this.loading()) { this.form.markAllAsTouched(); return; }
    const value = this.form.getRawValue();
    if (value.password !== value.confirmPassword) { this.error.set('Passwords do not match.'); return; }
    this.loading.set(true); this.error.set('');
    this.auth.register({
      first_name: value.first_name, last_name: value.last_name, email: value.email,
      phone_number: value.phone_number, password: value.password,
      date_of_birth: value.date_of_birth || null,
    }).subscribe({
      next: () => void this.router.navigateByUrl('/dashboard'),
      error: (response) => { this.error.set(response.error?.detail ?? 'Unable to create the account.'); this.loading.set(false); },
    });
  }
}
