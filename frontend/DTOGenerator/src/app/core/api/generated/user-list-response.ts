import type { UserRead } from './user-read';

export interface UserListResponse {
  message: string;
  data?: Array<UserRead>;
  count?: number;
}
