import type { TransactionStatus } from './transaction-status';

export interface TransactionUpdate {
  status?: TransactionStatus | null;
  description?: string | null;
  completed_at?: string | null;
}
