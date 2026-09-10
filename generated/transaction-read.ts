import type { TransactionStatus } from './transaction-status';
import type { TransactionType } from './transaction-type';

export interface TransactionRead {
  transaction_type: TransactionType;
  amount: string;
  currency_code: string;
  description?: string | null;
  id: string;
  reference: string;
  status: TransactionStatus;
  source_account_id: string | null;
  destination_account_id: string | null;
  fee: string;
  initiated_at: string;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
}
