# Quick Start Guide - GraphQL CRM

This guide will help you get the GraphQL CRM system up and running in minutes.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

## Installation

### Option 1: Automated Setup (Recommended)

```bash
# Clone the repository
git clone https://github.com/reuben-idan/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm

# Run the automated setup script
python setup.py
```

The setup script will:

- Install all dependencies
- Run database migrations
- Create a superuser account
- Seed the database with sample data

### Option 2: Manual Setup

```bash
# Clone the repository
git clone https://github.com/reuben-idan/alx-backend-graphql_crm.git
cd alx-backend-graphql_crm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed database with sample data
python seed_db.py

# Start the development server
python manage.py runserver
```

## Access Points

Once the server is running, you can access:

| Service                | URL                           | Description             |
| ---------------------- | ----------------------------- | ----------------------- |
| **GraphQL Playground** | http://127.0.0.1:8000/graphql | Interactive GraphQL IDE |
| **Django Admin**       | http://127.0.0.1:8000/admin   | Admin interface         |

## Sample GraphQL Queries

### 1. Fetch All Customers

```graphql
query {
  customers {
    edges {
      node {
        id
        name
        email
        phone
        totalOrders
        totalSpent
      }
    }
  }
}
```

### 2. Create a New Customer

```graphql
mutation {
  createCustomer(
    input: {
      name: "John Smith"
      email: "john.smith@example.com"
      phone: "+1234567890"
      address: "123 Main St, City, State"
    }
  ) {
    customer {
      id
      name
      email
    }
    success
    errors
  }
}
```

### 3. Search Products

```graphql
query {
  searchProducts(query: "laptop") {
    id
    name
    description
    price
    stockQuantity
    sku
  }
}
```

### 4. Get Order with Items

```graphql
query {
  orders {
    edges {
      node {
        id
        status
        orderDate
        totalAmount
        customer {
          name
          email
        }
        items {
          edges {
            node {
              quantity
              unitPrice
              subtotal
              product {
                name
                price
              }
            }
          }
        }
      }
    }
  }
}
```

## Project Structure

```
alx-backend-graphql_crm/
├── crm/                    # Main CRM application
│   ├── models.py          # Django models
│   ├── schema.py          # GraphQL schema
│   ├── admin.py           # Django admin
│   └── tests.py           # Unit tests
├── crm_project/           # Django project settings
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── seed_db.py            # Database seeding script
├── setup.py              # Automated setup script
└── README.md             # Project documentation
```

## Key Features

- **Customer Management**: Create, read, update, delete customers
- **Product Catalog**: Manage products with inventory tracking
- **Order Processing**: Handle orders with line items
- **GraphQL API**: Full GraphQL implementation with queries and mutations
- **Filtering & Search**: Advanced filtering capabilities
- **Pagination**: Relay-style cursor-based pagination
- **Admin Interface**: Django admin for data management

## Next Steps

1. **Explore the GraphQL Playground**: Try different queries and mutations
2. **Check the Admin Interface**: Manage data through Django admin
3. **Read the Full Documentation**: See README.md for detailed API documentation
4. **Run Tests**: Execute `python manage.py test` to run unit tests
5. **Customize**: Modify models, schema, and business logic as needed

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port with `python manage.py runserver 8001`
2. **Database errors**: Delete `db.sqlite3` and run migrations again
3. **Import errors**: Make sure you're in the correct directory and virtual environment is activated

### Getting Help

- Check the [README.md](README.md) for detailed documentation
- Review the GraphQL schema in `crm/schema.py`
- Examine the Django models in `crm/models.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Happy coding! 🚀**
