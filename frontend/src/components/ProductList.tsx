import React from "react";
import { useStore } from "../context/StoreContext";
import { Item } from "../types";

const ProductList: React.FC = () => {
  const { items, categories, fetchItems, addToCart } = useStore();

  return (
    <div className="product-list">
      <h2>Products</h2>
      <div className="categories">
        <button onClick={() => fetchItems()}>All</button>
        {categories.map((category) => (
          <button key={category} onClick={() => fetchItems(category)}>
            {category}
          </button>
        ))}
      </div>
      <div className="items">
        {items.map((item: Item) => (
          <div key={item.id} className="product">
            <h3>{item.name}</h3>
            <p>${item.price.toFixed(2)}</p>
            <p>{item.description}</p>
            <button onClick={() => addToCart(item.id, 1)}>Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductList;
