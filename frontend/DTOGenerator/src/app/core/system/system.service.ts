import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../api/api.config';

export interface ServiceHealth { message?: string; error?: string; }

@Injectable({ providedIn: 'root' })
export class SystemService {
  private readonly http = inject(HttpClient);

  heartbeat(): Observable<ServiceHealth> { return this.http.get<ServiceHealth>(API_BASE_URL); }
  database(): Observable<ServiceHealth> { return this.http.get<ServiceHealth>(`${API_BASE_URL}/db`); }
  openApi(): Observable<unknown> { return this.http.get<unknown>(`${API_BASE_URL}/openapi`); }
}
