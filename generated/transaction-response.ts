import type { TransactionRead } from './transaction-read';

export interface TransactionResponse {
  message: string;
  data?: TransactionRead | null;
}
