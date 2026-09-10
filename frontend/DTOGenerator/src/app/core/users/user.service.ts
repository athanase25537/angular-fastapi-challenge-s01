import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../api/api.config';
import type { UserCreate, UserListResponse, UserResponse, UserUpdate } from '../api/generated';

@Injectable({ providedIn: 'root' })
export class UserService {
  private readonly http = inject(HttpClient);

  create(payload: UserCreate): Observable<UserResponse> {
    return this.http.post<UserResponse>(`${API_BASE_URL}/user/create`, payload);
  }

  list(skip = 0, limit = 100): Observable<UserListResponse> {
    const params = new HttpParams().set('skip', skip).set('limit', limit);
    return this.http.get<UserListResponse>(`${API_BASE_URL}/user/list`, { params });
  }

  get(id: string): Observable<UserResponse> {
    return this.http.get<UserResponse>(`${API_BASE_URL}/user/${id}`);
  }

  update(id: string, payload: UserUpdate): Observable<UserResponse> {
    return this.http.put<UserResponse>(`${API_BASE_URL}/user/${id}`, payload);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${API_BASE_URL}/user/${id}`);
  }
}
