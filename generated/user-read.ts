import type { UserStatus } from './user-status';

export interface UserRead {
  email: string;
  phone_number: string;
  first_name: string;
  last_name: string;
  date_of_birth?: string | null;
  id: string;
  status: UserStatus;
  created_at: string;
  updated_at: string;
}
