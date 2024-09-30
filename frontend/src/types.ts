export interface Item {
    id: string;
    name: string;
    price: number;
    description: string;
    category: string;
  }
  
  export interface CartItem {
    id: string;
    name: string;
    price: number;
    quantity: number;
  }
  
  export interface DiscountStatus {
    status: boolean;
    message: string;
  }

  export interface Cart {
    items: CartItem[];
    total: number;
  }
  
  export interface Order {
    order_id: string;
    total: number;
    discount_amount: number;
    discount_status: DiscountStatus
  }
  
  export interface Stats {
    total_items: number;
    total_amount: number;
    discount_codes: string[];
    total_discount: number;
    order_count: number;
  }