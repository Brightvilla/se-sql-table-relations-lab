# SQL Table Relations Lab

Practice SQL JOIN operations using a SQLite database (`data.sqlite`) with 8 related tables: `employees`, `offices`, `customers`, `orders`, `orderdetails`, `payments`, `products`, and `productlines`.

## Setup

```bash
pip install pandas
```

## Run

```bash
python3 main.py
```

## Tests

```bash
pytest -v
```

## Steps

Each step in `main.py` builds a DataFrame using a SQL query:

| Step | Variable | Description |
|------|----------|-------------|
| 1 | `df_boston` | Employees working in the Boston office |
| 2 | `df_zero_emp` | Offices with no employees |
| 3 | `df_employee` | All employees with their office city and state |
| 4 | `df_contacts` | Customers who have never placed an order |
| 5 | `df_payment` | Customers and their payments, sorted by amount descending |
| 6 | `df_credit` | Sales reps whose customers have an average credit limit above $90,000 |
| 7 | `df_product_sold` | Products with total orders and units sold |
| 8 | `df_total_customers` | Products with count of unique customers who purchased them |
| 9 | `df_customers` | Number of customers per office |
| 10 | `df_under_20` | Employees who sold products purchased by fewer than 20 unique customers |

## Database Schema

```
employees   → offices        (officeCode)
employees   → customers      (salesRepEmployeeNumber)
customers   → orders         (customerNumber)
customers   → payments       (customerNumber)
orders      → orderdetails   (orderNumber)
orderdetails→ products       (productCode)
products    → productlines   (productLine)
```
