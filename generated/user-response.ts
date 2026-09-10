import type { UserRead } from './user-read';

export interface UserResponse {
  message: string;
  data?: UserRead | null;
}
