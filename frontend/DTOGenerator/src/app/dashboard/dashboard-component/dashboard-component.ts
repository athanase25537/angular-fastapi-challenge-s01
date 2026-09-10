import { CurrencyPipe, DatePipe, TitleCasePipe } from '@angular/common';
import { Component, ChangeDetectionStrategy, computed, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { TransactionService } from '../../core/transactions/transaction.service';
import { SystemService } from '../../core/system/system.service';
import type { TransactionRead } from '../../core/api/generated';

@Component({
  selector: 'app-dashboard-component',
  standalone: true,
  imports: [RouterLink, CurrencyPipe, DatePipe, TitleCasePipe],
  templateUrl: './dashboard-component.html',
  styleUrl: './dashboard-component.css',
  changeDetection: ChangeDetectionStrategy.Default,
})
export class DashboardComponent {
  readonly auth = inject(AuthService);
  private readonly transactionsApi = inject(TransactionService);
  private readonly systemApi = inject(SystemService);
  readonly transactions = signal<TransactionRead[]>([]);
  readonly loading = signal(true);
  readonly servicesOnline = signal(false);
  readonly databaseOnline = signal(false);
  readonly totalTransactions = computed(() => this.transactions().length);
  readonly pendingTransactions = computed(() => this.transactions().filter((item) => item.status === 'pending').length);
  readonly totalVolume = computed(() => this.transactions().reduce((sum, item) => sum + Number(item.amount), 0));
  readonly recentTransactions = computed(() => [...this.transactions()]
    .sort((a, b) => new Date(b.initiated_at).getTime() - new Date(a.initiated_at).getTime()).slice(0, 4));

  constructor() { this.refresh(); }

  refresh(): void {
    this.loading.set(true);
    this.transactionsApi.list({ limit: 100 }).subscribe({
      next: (response) => { this.transactions.set(response.data ?? []); this.loading.set(false); },
      error: () => this.loading.set(false),
    });
    this.systemApi.heartbeat().subscribe({ next: (response) => this.servicesOnline.set(!response.error), error: () => this.servicesOnline.set(false) });
    this.systemApi.database().subscribe({ next: (response) => this.databaseOnline.set(!response.error), error: () => this.databaseOnline.set(false) });
  }
}
