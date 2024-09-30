# Uniblox Assignment

A Flask-based RESTful API for a simple e-commerce platform. It provides endpoints for managing products, shopping carts, orders, and discount codes.

## Features

- Product Management
- List and filter products by category
- Shopping Cart
- Manage user shopping carts
- Order Processing
- Handle checkout and order creation
- Discount Codes
- Generate and apply discount codes
- Admin Statistics
- View basic store statistics

Clone the repository:

```bash
git clone https://github.com/ayamdobhal/uniblox-assignment.git
cd uniblox-assignment
```

## Backend

The Backend is written in Python using Flask.

### Prerequisites

- Python 3.7+
- Flask
- Flask-CORS

### Installation

Change to the backend directory:

```bash
cd backend
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the API server with:

```bash
python app.py
```

The API will be available at http://localhost:2000.

### API Endpoints

#### Products

| Method |    Endpoint     | Description                                 |
| ------ | :-------------: | :------------------------------------------ |
| GET    |   /api/items    | Retrieve all products or filter by category |
| GET    | /api/categories | Get all product categories                  |

#### Shopping Cart

| Method |     Endpoint     | Description                   |
| ------ | :--------------: | :---------------------------- |
| GET    |    /api/cart     | Get contents of a user's cart |
| POST   |  /api/cart/add   | Add an item to the cart       |
| POST   | /api/cart/remove | Remove an item from the cart  |

#### Checkout

| Method |   Endpoint    | Description                          |
| ------ | :-----------: | :----------------------------------- |
| POST   | /api/checkout | Process checkout and create an order |

#### Admin

| Method |           Endpoint           | Description                  |
| ------ | :--------------------------: | :--------------------------- |
| POST   | /api/admin/generate-discount | Generate a new discount code |
| GET    |       /api/admin/stats       | Get store statistics         |

### Development

The project uses Flask and Flask-CORS with a modular structure. To extend functionality:

- Add new models in the appropriate section.
- Create new routes in the API.
- Update the Store class as needed.
- Testing

### Testing

Testing is handled using `pytests`, to run tests:

First install the test requirements:

```bash
pip install -r test-requirements.txt
```

Then run the tests:

```bash
pytest test_app.py
```

## Frontend

The Frontend uses React.js.

### Prerequisites

- NodeJS 20
- Npm or Yarn or Pnpm

### Installation

Change to the frontend directory:

```bash
cd frontend
```

Install the requirements:

```bash
yarn
```

To start the frontend server, run:

```bash
yarn start
```

The frontend server will be available at http://localhost:3000.

![Frontend](https://cdn.discordapp.com/attachments/799886758837092352/1290281497109987448/image.png?ex=66fbe3c9&is=66fa9249&hm=c5bd998791394519252c472a430a42f461718c35b847bc6d6a3efe0cf4c192d5&)
