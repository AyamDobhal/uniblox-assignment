import React from "react";
import { useStore } from "../context/StoreContext";

const AdminPanel: React.FC = () => {
  const { generateDiscount, fetchStats, stats } = useStore();

  return (
    <div className="admin-panel">
      <h2>Admin Panel</h2>
      <button onClick={generateDiscount}>Generate Discount Code</button>
      <button onClick={fetchStats}>Fetch Stats</button>
      {stats && (
        <div className="stats">
          <p>Total Items Sold: {stats.total_items}</p>
          <p>Total Amount: ${stats.total_amount.toFixed(2)}</p>
          <p>Total Discount: ${stats.total_discount.toFixed(2)}</p>
          <p>Discount Codes: {stats.discount_codes.join(", ")}</p>
          <p>Order Count: {stats.order_count}</p>
        </div>
      )}
    </div>
  );
};

export default AdminPanel;
