import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../api/api.config';
import type { TransactionListResponse } from '../api/generated';

@Injectable({ providedIn: 'root' })
export class TransactionService {
  private readonly http = inject(HttpClient);

  list(): Observable<TransactionListResponse> {
    return this.http.get<TransactionListResponse>(`${API_BASE_URL}/transactions/list`);
  }
}
