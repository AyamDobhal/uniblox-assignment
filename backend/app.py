import uuid
from typing import List, Mapping, Optional, Union

from flask import Flask, jsonify, request
from flask_cors import CORS

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# Models
class Item:
    """Represents a product in the store."""

    def __init__(
        self, name: str, price: float, description: str, category: str
    ) -> None:
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.description = description
        self.category = category


class CartItem:
    """Represents an item in a user's cart."""

    def __init__(self, item: Item, quantity: int) -> None:
        self.item = item
        self.quantity = quantity


class Cart:
    """Represents a user's shopping cart."""

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.items: List[CartItem] = []

    def add_item(self, item: Item, quantity: int) -> None:
        """Add an item to the cart or update its quantity if it already exists."""
        for cart_item in self.items:
            if cart_item.item.id == item.id:
                cart_item.quantity += quantity
                return
        self.items.append(CartItem(item, quantity))

    def remove_item(self, item_id: str) -> None:
        """Remove an item from the cart."""
        self.items = [item for item in self.items if item.item.id != item_id]

    def clear(self) -> None:
        """Clear all items from the cart."""
        self.items = []

    @property
    def total(self) -> float:
        """Calculate the total price of all items in the cart."""
        return sum(item.item.price * item.quantity for item in self.items)


class DiscountStatus:
    """Represents the status of a discount application."""

    def __init__(
        self, status: bool = False, message: str = "No discount code applied."
    ) -> None:
        self.status = status
        self.message = message

    @property
    def getstats(self) -> Mapping[str, Union[bool, str]]:
        """Get the discount status as a dictionary."""
        return {"status": self.status, "message": self.message}


class Order:
    """Represents a user's order."""

    def __init__(self, user_id: str, items: List[CartItem], total: float) -> None:
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = items
        self.total = total
        self.discount_status = DiscountStatus()
        self.discount_code: Optional[str] = None
        self.discount_amount: float = 0

    def items_count(self) -> int:
        """Get the total number of items in the order."""
        return sum(item.quantity for item in self.items)


class DiscountCode:
    """Represents a discount code."""

    def __init__(self, code: str, percentage: float) -> None:
        self.code = code
        self.percentage = percentage
        self.used = False


class Stats:
    """Represents store statistics."""

    def __init__(
        self,
        total_items: int,
        total_amount: float,
        discount_codes: List[str],
        total_discount: float,
        order_count: int,
    ) -> None:
        self.total_items = total_items
        self.total_amount = total_amount
        self.discount_codes = discount_codes
        self.total_discount = total_discount
        self.order_count = order_count

    def get_json(self) -> dict:
        """Get the stats as a dictionary."""
        return {
            "total_items": self.total_items,
            "total_amount": self.total_amount,
            "discount_codes": self.discount_codes,
            "total_discount": self.total_discount,
            "order_count": self.order_count,
        }


class Store:
    """Represents the e-commerce store."""

    def __init__(self) -> None:
        self.items: dict[str, Item] = {}
        self.carts: dict[str, Cart] = {}
        self.orders: List[Order] = []
        self.discount_codes: List[DiscountCode] = []
        self.order_count: int = 0
        self.n: int = 5  # Number of orders after which a discount code is generated

    def add_item(self, item: Item) -> None:
        """Add an item to the store inventory."""
        self.items[item.id] = item

    def get_cart(self, user_id: str) -> Cart:
        """Get a user's cart, creating a new one if it doesn't exist."""
        if user_id not in self.carts:
            self.carts[user_id] = Cart(user_id)
        return self.carts[user_id]

    def create_order(self, user_id: str, discount_code: Optional[str] = None) -> Order:
        """Create a new order for a user."""
        cart = self.get_cart(user_id)
        order = Order(user_id, cart.items, cart.total)

        if discount_code:
            order.discount_status = self.apply_discount(order, discount_code)

        self.orders.append(order)
        self.order_count += 1

        if self.order_count % self.n == 0:
            self.generate_discount_code()

        self.carts[user_id].clear()
        return order

    def generate_discount_code(self) -> None:
        """Generate a new discount code."""
        code = f"DISCOUNT{len(self.discount_codes) + 1}"
        self.discount_codes.append(DiscountCode(code, 0.1))

    def apply_discount(self, order: Order, discount_code: str) -> DiscountStatus:
        """Apply a discount code to an order."""
        if not self.can_apply_discount:
            return DiscountStatus(False, "Discount code cannot be applied right now.")
        for code in self.discount_codes:
            if code.code == discount_code and not code.used:
                order.discount_code = code.code
                order.discount_amount = order.total * code.percentage
                order.total -= order.discount_amount
                code.used = True
                return DiscountStatus(True, code.code)
        return DiscountStatus(False, "Invalid discount code.")

    def get_stats(self) -> dict:
        """Get store statistics."""
        total_items = sum(order.items_count() for order in self.orders)
        total_amount = sum(order.total for order in self.orders)
        total_discount = sum(
            order.discount_amount for order in self.orders if order.discount_amount
        )
        return Stats(
            total_items,
            total_amount,
            [code.code for code in self.discount_codes],
            total_discount,
            self.order_count,
        ).get_json()

    @property
    def can_apply_discount(self) -> bool:
        """Check if a discount can be applied based on the order count."""
        return self.order_count > 1 and (self.order_count + 1) % self.n == 0


# Initialize store and add sample products
store = Store()

products = [
    Item("Smartphone", 599.99, "Latest model with advanced features", "Electronics"),
    Item(
        "Laptop", 999.99, "High-performance laptop for work and gaming", "Electronics"
    ),
    Item(
        "Wireless Earbuds",
        129.99,
        "True wireless earbuds with noise cancellation",
        "Electronics",
    ),
    Item("Running Shoes", 89.99, "Comfortable shoes for jogging and running", "Sports"),
    Item("Yoga Mat", 29.99, "Non-slip yoga mat for home workouts", "Sports"),
    Item("Protein Powder", 39.99, "Whey protein for muscle recovery", "Health"),
    Item("Multivitamins", 19.99, "Daily multivitamin supplement", "Health"),
    Item("Novel", 14.99, "Bestselling fiction novel", "Books"),
    Item("Cookbook", 24.99, "Collection of gourmet recipes", "Books"),
    Item(
        "Coffee Maker", 79.99, "Programmable coffee maker with thermal carafe", "Home"
    ),
    Item("Blender", 49.99, "High-speed blender for smoothies and more", "Home"),
    Item("Backpack", 59.99, "Durable backpack for daily use or travel", "Fashion"),
]

for product in products:
    store.add_item(product)


# API Routes
@app.route("/api/items", methods=["GET"])
def get_items():
    """Get all items or filter by category."""
    category = request.args.get("category")
    items = store.items.values()
    if category:
        items = [item for item in items if item.category.lower() == category.lower()]
    return jsonify(
        [
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "description": item.description,
                "category": item.category,
            }
            for item in items
        ]
    )


@app.route("/api/categories", methods=["GET"])
def get_categories():
    """Get all unique categories."""
    categories = set(item.category for item in store.items.values())
    return jsonify(list(categories))


@app.route("/api/cart", methods=["GET"])
def get_cart():
    """Get the contents of a user's cart."""
    user_id = request.args.get("user_id")
    cart = store.get_cart(user_id)
    return jsonify(
        {
            "items": [
                {
                    "id": item.item.id,
                    "name": item.item.name,
                    "price": item.item.price,
                    "quantity": item.quantity,
                }
                for item in cart.items
            ],
            "total": cart.total,
        }
    )


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    """Add an item to a user's cart."""
    data = request.json
    user_id = data["user_id"]
    item_id = data["item_id"]
    quantity = data["quantity"]

    item = store.items.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    cart = store.get_cart(user_id)
    cart.add_item(item, quantity)
    return jsonify({"message": "Item added to cart"})


@app.route("/api/cart/remove", methods=["POST"])
def remove_from_cart():
    """Remove an item from a user's cart."""
    data = request.json
    user_id = data["user_id"]
    item_id = data["item_id"]

    cart = store.get_cart(user_id)
    cart.remove_item(item_id)
    return jsonify({"message": "Item removed from cart"})


@app.route("/api/checkout", methods=["POST"])
def checkout():
    """Process a checkout, creating a new order."""
    data = request.json
    user_id = data["user_id"]
    discount_code = data.get("discount_code")

    order = store.create_order(user_id, discount_code)
    return jsonify(
        {
            "order_id": order.id,
            "total": order.total,
            "discount_amount": order.discount_amount,
            "discount_status": order.discount_status.getstats,
        }
    )


@app.route("/api/admin/generate-discount", methods=["POST"])
def generate_discount():
    """Generate a new discount code."""
    store.generate_discount_code()
    return jsonify({"message": "Discount code generated"})


@app.route("/api/admin/stats", methods=["GET"])
def get_stats():
    """Get store statistics."""
    return jsonify(store.get_stats())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=2000)
