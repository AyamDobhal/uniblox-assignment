import json

import pytest
from app import Item, app, store


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_items(client):
    response = client.get("/api/items")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 12  # Assuming all 12 sample products are added


def test_get_items_by_category(client):
    response = client.get("/api/items?category=Electronics")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert all(item["category"] == "Electronics" for item in data)


def test_get_categories(client):
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert set(data) == {"Electronics", "Sports", "Health", "Books", "Home", "Fashion"}


def test_get_cart(client):
    response = client.get("/api/cart?user_id=test_user")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "items" in data
    assert "total" in data


def test_add_to_cart(client):
    item = next(iter(store.items.values()))
    response = client.post(
        "/api/cart/add",
        json={"user_id": "test_user", "item_id": item.id, "quantity": 2},
    )
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Item added to cart"


def test_remove_from_cart(client):
    # First, add an item to the cart
    item = next(iter(store.items.values()))
    client.post(
        "/api/cart/add",
        json={"user_id": "test_user", "item_id": item.id, "quantity": 1},
    )

    # Then remove it
    response = client.post(
        "/api/cart/remove", json={"user_id": "test_user", "item_id": item.id}
    )
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Item removed from cart"


def test_checkout(client):
    # Add an item to the cart first
    item = next(iter(store.items.values()))
    client.post(
        "/api/cart/add",
        json={"user_id": "test_user", "item_id": item.id, "quantity": 1},
    )

    response = client.post("/api/checkout", json={"user_id": "test_user"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "order_id" in data
    assert "total" in data
    assert "discount_amount" in data
    assert "discount_status" in data


def test_generate_discount(client):
    response = client.post("/api/admin/generate-discount")
    assert response.status_code == 200
    assert json.loads(response.data)["message"] == "Discount code generated"


def test_get_stats(client):
    response = client.get("/api/admin/stats")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "total_items" in data
    assert "total_amount" in data
    assert "discount_codes" in data
    assert "total_discount" in data
    assert "order_count" in data


def test_discount_application():
    # Create a new store for this test
    test_store = store.__class__()

    # Add a sample item
    item = Item("Test Item", 100.0, "Test Description", "Test Category")
    test_store.add_item(item)

    # Create 5 orders to generate a discount code
    for _ in range(5):
        test_store.create_order("test_user")

    for _ in range(4):
        test_store.create_order("test_user")

    # Get the generated discount code
    discount_code = test_store.discount_codes[-1]

    # Create a new order with the discount code
    cart = test_store.get_cart("test_user")
    cart.add_item(item, 1)
    order = test_store.create_order("test_user", discount_code.code)

    assert order.discount_amount == 10.0  # 10% of 100
    assert order.total == 90.0
    assert order.discount_status.status == True


def test_cannot_apply_discount_before_nth_order():
    test_store = store.__class__()
    item = Item("Test Item", 100.0, "Test Description", "Test Category")
    test_store.add_item(item)

    # Create 4 orders (less than n=5)
    for _ in range(4):
        test_store.create_order("test_user")

    # Try to apply a non-existent discount code
    cart = test_store.get_cart("test_user")
    cart.add_item(item, 1)
    order = test_store.create_order("test_user", "INVALID_CODE")

    assert order.discount_amount == 0
    assert order.total == 100.0
    assert order.discount_status.status == False
