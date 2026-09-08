import type { TransactionType } from './transaction-type';

export interface TransactionCreate {
  transaction_type: TransactionType;
  amount: number | string;
  currency_code: string;
  description?: string | null;
  source_account_id?: string | null;
  destination_account_id?: string | null;
}
