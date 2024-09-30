import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";
import api from "../api/axiosConfig";
import { Cart, Item, Order, Stats } from "../types";

interface StoreContextType {
  items: Item[];
  cart: Cart;
  categories: string[];
  stats: Stats | null;
  fetchItems: (category?: string) => Promise<void>;
  addToCart: (itemId: string, quantity: number) => Promise<void>;
  removeFromCart: (itemId: string) => Promise<void>;
  checkout: (discountCode?: string) => Promise<Order | null>;
  generateDiscount: () => Promise<void>;
  fetchStats: () => Promise<void>;
}

const StoreContext = createContext<StoreContextType | undefined>(undefined);

export const StoreProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [items, setItems] = useState<Item[]>([]);
  const [cart, setCart] = useState<Cart>({ items: [], total: 0 });
  const [categories, setCategories] = useState<string[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);

  const fetchItems = async (category?: string) => {
    try {
      const response = await api.get("/items", { params: { category } });
      setItems(response.data);
    } catch (error) {
      console.error("Error fetching items:", error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await api.get("/categories");
      setCategories(response.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  const fetchCart = async () => {
    try {
      const response = await api.get("/cart", { params: { user_id: "user1" } });
      setCart(response.data);
    } catch (error) {
      console.error("Error fetching cart:", error);
    }
  };

  const addToCart = async (itemId: string, quantity: number) => {
    try {
      await api.post("/cart/add", {
        user_id: "user1",
        item_id: itemId,
        quantity,
      });
      await fetchCart();
    } catch (error) {
      console.error("Error adding to cart:", error);
    }
  };

  const removeFromCart = async (itemId: string) => {
    try {
      await api.post("/cart/remove", { user_id: "user1", item_id: itemId });
      await fetchCart();
    } catch (error) {
      console.error("Error removing from cart:", error);
    }
  };

  const checkout = async (discountCode?: string): Promise<Order | null> => {
    try {
      const response = await api.post("/checkout", {
        user_id: "user1",
        discount_code: discountCode,
      });
      await fetchCart();
      return response.data;
    } catch (error) {
      console.error("Error during checkout:", error);
      return null;
    }
  };

  const generateDiscount = async () => {
    try {
      await api.post("/admin/generate-discount");
    } catch (error) {
      console.error("Error generating discount:", error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await api.get("/admin/stats");
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  useEffect(() => {
    fetchItems();
    fetchCategories();
    fetchCart();
  }, []);

  return (
    <StoreContext.Provider
      value={{
        items,
        cart,
        categories,
        stats,
        fetchItems,
        addToCart,
        removeFromCart,
        checkout,
        generateDiscount,
        fetchStats,
      }}
    >
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => {
  const context = useContext(StoreContext);
  if (context === undefined) {
    throw new Error("useStore must be used within a StoreProvider");
  }
  return context;
};
