import type { UserRead } from './user-read';

export interface TokenResponse {
  access_token: string;
  token_type?: string;
  user: UserRead;
}
