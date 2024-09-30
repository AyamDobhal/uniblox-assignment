import React, { useState } from "react";
import { useStore } from "../context/StoreContext";

const Cart: React.FC = () => {
  const { cart, removeFromCart, checkout } = useStore();
  const [discountCode, setDiscountCode] = useState("");

  const handleCheckout = async () => {
    const order = await checkout(discountCode);
    if (order) {
      alert(
        `Order placed! Total: $${order.total.toFixed(2)}, ${
          order.discount_status.status
            ? `Discount: $${order.discount_amount.toFixed(2)}`
            : order.discount_status.message
        }`
      );
    } else {
      alert("Error during checkout");
    }
  };

  return (
    <div className="cart">
      <h2>Cart</h2>
      {cart.items.map((item) => (
        <div key={item.id} className="cart-item">
          <span>
            {item.name} - ${item.price.toFixed(2)} x {item.quantity}
          </span>
          <button onClick={() => removeFromCart(item.id)}>Remove</button>
        </div>
      ))}
      <p>Total: ${cart.total.toFixed(2)}</p>
      <input
        type="text"
        placeholder="Discount Code"
        value={discountCode}
        onChange={(e) => setDiscountCode(e.target.value)}
      />
      <button onClick={handleCheckout}>Checkout</button>
    </div>
  );
};

export default Cart;
