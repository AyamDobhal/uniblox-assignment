import React from "react";
import "./App.css";
import AdminPanel from "./components/AdminPanel";
import Cart from "./components/Cart";
import ProductList from "./components/ProductList";

const App: React.FC = () => {
  return (
    <div className="App">
      <h1>E-commerce Store</h1>
      <ProductList />
      <Cart />
      <AdminPanel />
    </div>
  );
};

export default App;
