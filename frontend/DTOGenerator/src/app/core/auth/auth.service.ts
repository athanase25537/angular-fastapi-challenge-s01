import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Injectable, PLATFORM_ID, inject, signal } from '@angular/core';
import { Observable, tap } from 'rxjs';
import { API_BASE_URL } from '../api/api.config';
import type { LoginRequest, TokenResponse, UserCreate, UserRead } from '../api/generated';

const TOKEN_KEY = 's01.access-token';
const USER_KEY = 's01.user';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly platformId = inject(PLATFORM_ID);
  readonly token = signal<string | null>(this.readStorage(TOKEN_KEY));
  readonly user = signal<UserRead | null>(this.readStoredUser());
  readonly isAuthenticated = () => this.token() !== null;

  login(payload: LoginRequest): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${API_BASE_URL}/auth/login`, payload).pipe(tap((result) => this.persist(result)));
  }

  register(payload: UserCreate): Observable<TokenResponse> {
    return this.http.post<TokenResponse>(`${API_BASE_URL}/auth/register`, payload).pipe(tap((result) => this.persist(result)));
  }

  refreshProfile(): Observable<UserRead> {
    return this.http.get<UserRead>(`${API_BASE_URL}/auth/me`).pipe(tap((user) => this.persistUser(user)));
  }

  logout(): void {
    this.token.set(null);
    this.user.set(null);
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
    }
  }

  private persist(result: TokenResponse): void {
    this.token.set(result.access_token);
    this.user.set(result.user);
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(TOKEN_KEY, result.access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(result.user));
    }
  }

  private persistUser(user: UserRead): void {
    this.user.set(user);
    if (isPlatformBrowser(this.platformId)) localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  private readStorage(key: string): string | null {
    return isPlatformBrowser(this.platformId) ? localStorage.getItem(key) : null;
  }

  private readStoredUser(): UserRead | null {
    const value = this.readStorage(USER_KEY);
    if (!value) return null;
    try { return JSON.parse(value) as UserRead; } catch { return null; }
  }
}
