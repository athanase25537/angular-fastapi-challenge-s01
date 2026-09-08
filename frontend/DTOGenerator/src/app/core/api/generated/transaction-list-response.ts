import type { TransactionRead } from './transaction-read';

export interface TransactionListResponse {
  message: string;
  data?: Array<TransactionRead>;
  count?: number;
}
