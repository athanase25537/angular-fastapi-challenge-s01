export interface UserCreate {
  email: string;
  phone_number: string;
  first_name: string;
  last_name: string;
  date_of_birth?: string | null;
  password: string;
}
