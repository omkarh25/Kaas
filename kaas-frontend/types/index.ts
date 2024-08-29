export interface Asset {
    id: number;
    name: string;
    amount: number;
    department: string;
    comments: string;
  }
  
  export interface Transaction {
    id: number;
    date: string;
    description: string;
    amount: number;
    payment_mode: string;
    acc_id: string;
    department: string;
    comments: string | null;
    category: string;
    payment_mode_detail: string;
    zoho_match: boolean;
  }