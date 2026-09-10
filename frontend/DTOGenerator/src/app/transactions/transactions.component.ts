import { Component, ChangeDetectionStrategy, inject, signal } from '@angular/core';
import { CurrencyPipe, DatePipe, TitleCasePipe } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { TransactionService } from '../core/transactions/transaction.service';
import type { TransactionRead, TransactionStatus, TransactionType } from '../core/api/generated';

@Component({
  selector: 'app-transactions', imports: [ReactiveFormsModule, DatePipe, CurrencyPipe, TitleCasePipe],
  templateUrl: './transactions.component.html', styleUrl: './transactions.component.css', changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TransactionsComponent {
  private readonly transactionsApi = inject(TransactionService); private readonly fb = inject(FormBuilder);
  readonly transactions = signal<TransactionRead[]>([]); readonly selected = signal<TransactionRead | null>(null);
  readonly loading = signal(true); readonly saving = signal(false); readonly error = signal(''); readonly notice = signal(''); readonly createOpen = signal(false); readonly total = signal(0);
  readonly statuses: TransactionStatus[] = ['pending', 'completed', 'failed', 'cancelled', 'reversed'];
  readonly types: TransactionType[] = ['deposit', 'withdrawal', 'transfer', 'payment', 'card_payment', 'fee', 'interest', 'refund'];
  readonly filterForm = this.fb.nonNullable.group({ status: [''], transactionType: [''] });
  readonly lookupForm = this.fb.nonNullable.group({ mode: ['reference'], value: [''] });
  readonly createForm = this.fb.nonNullable.group({ transaction_type: ['payment' as TransactionType, Validators.required], amount: ['', [Validators.required, Validators.min(0.01)]], currency_code: ['USD', [Validators.required, Validators.pattern(/^[a-zA-Z]{3}$/)]], description: [''], source_account_id: [''], destination_account_id: [''] });
  readonly updateForm = this.fb.nonNullable.group({ status: ['pending' as TransactionStatus], description: [''] });

  constructor() { this.load(); }
  load(): void {
    this.loading.set(true); this.error.set(''); const filters = this.filterForm.getRawValue();
    this.transactionsApi.list({ status: filters.status as TransactionStatus, transactionType: filters.transactionType as TransactionType }).subscribe({
      next: (response) => { this.transactions.set(response.data ?? []); this.total.set(response.count ?? response.data?.length ?? 0); this.loading.set(false); }, error: (response) => { this.error.set(this.message(response, 'Unable to load transactions.')); this.loading.set(false); },
    });
  }
  clearFilters(): void { this.filterForm.reset({ status: '', transactionType: '' }); this.load(); }
  inspect(transaction: TransactionRead): void { this.selected.set(transaction); this.updateForm.reset({ status: transaction.status, description: transaction.description ?? '' }); this.error.set(''); this.notice.set(''); }
  lookup(): void {
    const { mode, value } = this.lookupForm.getRawValue(); if (!value.trim()) return; this.loading.set(true); this.error.set('');
    if (mode === 'account') {
      this.transactionsApi.getByAccount(value.trim()).subscribe({ next: (response) => this.showLookup(response.data ?? []), error: (response) => this.lookupError(response) });
    } else {
      this.transactionsApi.getByReference(value.trim()).subscribe({ next: (response) => this.showLookup(response.data ? [response.data] : []), error: (response) => this.lookupError(response) });
    }
  }
  create(): void {
    if (this.createForm.invalid || this.saving()) { this.createForm.markAllAsTouched(); return; } this.saving.set(true); this.error.set(''); const value = this.createForm.getRawValue();
    this.transactionsApi.create({ ...value, amount: Number(value.amount), currency_code: value.currency_code.toUpperCase(), description: value.description || null, source_account_id: value.source_account_id || null, destination_account_id: value.destination_account_id || null }).subscribe({
      next: (response) => { this.saving.set(false); this.createOpen.set(false); this.notice.set(response.message); this.createForm.reset({ transaction_type: 'payment', amount: '', currency_code: 'USD', description: '', source_account_id: '', destination_account_id: '' }); this.load(); }, error: (response) => { this.saving.set(false); this.error.set(this.message(response, 'Unable to create transaction.')); },
    });
  }
  saveUpdate(): void {
    const item = this.selected(); if (!item || this.saving()) return; this.saving.set(true); this.error.set(''); const value = this.updateForm.getRawValue();
    this.transactionsApi.update(item.id, { status: value.status, description: value.description || null }).subscribe({ next: (response) => this.applyResponse(response.data, response.message), error: (response) => { this.saving.set(false); this.error.set(this.message(response, 'Unable to update transaction.')); } });
  }
  complete(): void { this.runAction('complete'); } cancel(): void { this.runAction('cancel'); }
  remove(): void {
    const item = this.selected(); if (!item || !confirm(`Delete ${item.reference}? This cannot be undone.`)) return; this.saving.set(true);
    this.transactionsApi.delete(item.id).subscribe({ next: () => { this.saving.set(false); this.selected.set(null); this.notice.set('Transaction deleted.'); this.load(); }, error: (response) => { this.saving.set(false); this.error.set(this.message(response, 'Only pending transactions can be deleted.')); } });
  }
  private runAction(action: 'complete' | 'cancel'): void {
    const item = this.selected(); if (!item || this.saving()) return; this.saving.set(true); this.error.set('');
    (action === 'complete' ? this.transactionsApi.complete(item.id) : this.transactionsApi.cancel(item.id)).subscribe({ next: (response) => this.applyResponse(response.data, response.message), error: (response) => { this.saving.set(false); this.error.set(this.message(response, `Unable to ${action} transaction.`)); } });
  }
  private applyResponse(item: TransactionRead | null | undefined, message: string): void { this.saving.set(false); this.notice.set(message); if (item) this.inspect(item); this.load(); }
  private showLookup(list: TransactionRead[]): void { this.transactions.set(list); this.total.set(list.length); this.loading.set(false); this.notice.set(`${list.length} matching transaction${list.length === 1 ? '' : 's'} found.`); }
  private lookupError(response: any): void { this.error.set(this.message(response, 'No matching transaction found.')); this.loading.set(false); }
  private message(response: any, fallback: string): string { return response.error?.detail ?? fallback; }
}
