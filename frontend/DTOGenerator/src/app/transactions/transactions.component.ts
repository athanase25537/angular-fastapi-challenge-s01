import { Component, ChangeDetectionStrategy, inject, signal } from '@angular/core';
import { DatePipe, DecimalPipe } from '@angular/common';
import { TransactionService } from '../core/transactions/transaction.service';
import type { TransactionRead } from '../core/api/generated';

@Component({
  selector: 'app-transactions',
  imports: [DatePipe, DecimalPipe],
  templateUrl: './transactions.component.html',
  styleUrl: './transactions.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TransactionsComponent {
  private readonly transactionsApi = inject(TransactionService);
  readonly transactions = signal<TransactionRead[]>([]);
  readonly loading = signal(true);
  readonly error = signal('');

  constructor() { this.load(); }

  load(): void {
    this.loading.set(true); this.error.set('');
    this.transactionsApi.list().subscribe({
      next: (response) => { this.transactions.set(response.data ?? []); this.loading.set(false); },
      error: (response) => { this.error.set(response.error?.detail ?? 'Unable to load transactions.'); this.loading.set(false); },
    });
  }
}
