import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../api/api.config';
import type {
  TransactionCreate,
  TransactionListResponse,
  TransactionResponse,
  TransactionStatus,
  TransactionType,
  TransactionUpdate,
} from '../api/generated';

@Injectable({ providedIn: 'root' })
export class TransactionService {
  private readonly http = inject(HttpClient);

  list(filters: { skip?: number; limit?: number; status?: TransactionStatus | ''; transactionType?: TransactionType | '' } = {}): Observable<TransactionListResponse> {
    let params = new HttpParams();
    if (filters.skip !== undefined) params = params.set('skip', filters.skip);
    if (filters.limit !== undefined) params = params.set('limit', filters.limit);
    if (filters.status) params = params.set('status', filters.status);
    if (filters.transactionType) params = params.set('transaction_type', filters.transactionType);
    return this.http.get<TransactionListResponse>(`${API_BASE_URL}/transactions/list`, { params });
  }

  create(payload: TransactionCreate): Observable<TransactionResponse> {
    return this.http.post<TransactionResponse>(`${API_BASE_URL}/transactions/create`, payload);
  }

  get(id: string): Observable<TransactionResponse> {
    return this.http.get<TransactionResponse>(`${API_BASE_URL}/transactions/${id}`);
  }

  getByReference(reference: string): Observable<TransactionResponse> {
    return this.http.get<TransactionResponse>(`${API_BASE_URL}/transactions/reference/${encodeURIComponent(reference)}`);
  }

  getByAccount(accountId: string): Observable<TransactionListResponse> {
    return this.http.get<TransactionListResponse>(`${API_BASE_URL}/transactions/account/${accountId}`);
  }

  update(id: string, payload: TransactionUpdate): Observable<TransactionResponse> {
    return this.http.put<TransactionResponse>(`${API_BASE_URL}/transactions/${id}`, payload);
  }

  complete(id: string): Observable<TransactionResponse> {
    return this.http.post<TransactionResponse>(`${API_BASE_URL}/transactions/${id}/complete`, {});
  }

  cancel(id: string): Observable<TransactionResponse> {
    return this.http.post<TransactionResponse>(`${API_BASE_URL}/transactions/${id}/cancel`, {});
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${API_BASE_URL}/transactions/${id}`);
  }
}
