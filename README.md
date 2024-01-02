# Invoice Management API

This Django Rest Framework project provides APIs for managing invoices and their details.

## Overview

The Invoice Management API allows you to:

- Create, retrieve, update, and delete invoices.
- Add, update, and remove details for each invoice.
- Get a list of all invoices or retrieve details for a specific invoice.

## Technologies Used

- Django: Web framework for building the API.
- Django Rest Framework: Toolkit for building Web APIs in Django.
- SQLite: Database engine for storing invoice and invoice detail data.
- Python: Programming language used for backend development.

## API Endpoints

### Get a list of all invoices:

- **URL:** `/invoices/`
- **HTTP Method:** GET

### Get details of a specific invoice:

- **URL:** `/invoices/<int:pk>/`
- **HTTP Method:** GET

### Delete an existing invoice:

- **URL:** `/invoices/<int:pk>/`
- **HTTP Method:** DELETE

### Create a new invoice:

- **URL:** `/invoices/`
- **HTTP Method:** POST
- **Payload Example:**

```json
{
  "date": "2022-01-01",
  "customer_name": "Test Customer",
  "details": [
    {
      "description": "Item 1",
      "quantity": 2,
      "unit_price": 5,
      "price": 10
    }
  ]
}
```
### Update an existing invoice:

- **URL:** `/invoices/<int:pk>/`
- **HTTP Method:** PATCH
- **Payload Example:**

  ```json
  {
  "date": "2022-01-02",
  "customer_name": "Updated Customer",
  "details": [
    {
      "id": 1,
      "description": "Updated Item",
      "quantity": 3,
      "unit_price": 15,
      "price": 45
     }
   ]
  }
