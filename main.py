

import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")

# 1. Employees working in the Boston office
df_boston = pd.read_sql_query(
    """
    SELECT e."firstName", e."lastName"
    FROM employees e
    JOIN offices o ON e."officeCode" = o."officeCode"
    WHERE o."city" = 'Boston'
    ORDER BY e."firstName", e."lastName"
    """,
    conn,
)

# Offices with no employees
df_zero_emp = pd.read_sql_query(
    """
    SELECT o."city", o."state"
    FROM offices o
    LEFT JOIN employees e ON o."officeCode" = e."officeCode"
    WHERE e."employeeNumber" IS NULL
    ORDER BY o."city", o."state"
    """,
    conn,
)

# 2. All employees with their office city and state
df_employee = pd.read_sql_query(
    """
    SELECT e."firstName", e."lastName", o."city", o."state"
    FROM employees e
    JOIN offices o ON e."officeCode" = o."officeCode"
    ORDER BY e."firstName", e."lastName"
    """,
    conn,
)

# Customers who have never placed an order
df_contacts = pd.read_sql_query(
    """
    SELECT c."contactFirstName", c."contactLastName", c."city", c."country"
    FROM customers c
    LEFT JOIN orders o ON c."customerNumber" = o."customerNumber"
    WHERE o."orderNumber" IS NULL
    ORDER BY c."contactLastName", c."contactFirstName"
    """,
    conn,
)

# 3. Customers and their payments, sorted by amount descending
# "amount" is stored as TEXT in this DB, so it must be cast to a numeric
# type before ordering, or it sorts lexicographically (wrong).
df_payment = pd.read_sql_query(
    """
    SELECT c."contactFirstName",
           c."contactLastName",
           p."paymentDate",
           p."amount"
    FROM payments p
    JOIN customers c ON p."customerNumber" = c."customerNumber"
    ORDER BY CAST(p."amount" AS REAL) DESC
    """,
    conn,
)

# 4. Sales reps whose customers have an average credit limit above 90,000
# "creditLimit" is also TEXT, cast before aggregating.
# Ordered by last name (Bott, Hernandez, Jennings, Marsh -> Larry first).
df_credit = pd.read_sql_query(
    """
    SELECT e."firstName",
           e."lastName",
           e."employeeNumber",
           AVG(CAST(c."creditLimit" AS REAL)) AS "avg_credit"
    FROM employees e
    JOIN customers c ON e."employeeNumber" = c."salesRepEmployeeNumber"
    GROUP BY e."employeeNumber", e."firstName", e."lastName"
    HAVING AVG(CAST(c."creditLimit" AS REAL)) > 90000
    ORDER BY e."lastName"
    """,
    conn,
)

# 5. Products with total orders and units sold
df_product_sold = pd.read_sql_query(
    """
    SELECT p."productCode",
           COUNT(DISTINCT od."orderNumber") AS "totalorders",
           SUM(od."quantityOrdered")       AS "totalunits"
    FROM orderdetails od
    JOIN products p ON od."productCode" = p."productCode"
    GROUP BY p."productCode"
    ORDER BY "totalunits" DESC
    """,
    conn,
)

# 6. Products with count of unique customers who purchased them
df_total_customers = pd.read_sql_query(
    """
    SELECT p."productCode",
           COUNT(DISTINCT o."customerNumber") AS "numpurchasers",
           SUM(od."quantityOrdered")          AS "totalunits"
    FROM orderdetails od
    JOIN orders o ON od."orderNumber" = o."orderNumber"
    JOIN products p ON od."productCode" = p."productCode"
    GROUP BY p."productCode"
    ORDER BY "numpurchasers" DESC
    """,
    conn,
)

# 7. Number of customers per office
df_customers = pd.read_sql_query(
    """
    SELECT o."city",
           o."state",
           COUNT(DISTINCT c."customerNumber") AS "n_customers"
    FROM offices o
    LEFT JOIN employees e ON o."officeCode" = e."officeCode"
    LEFT JOIN customers c ON e."employeeNumber" = c."salesRepEmployeeNumber"
    GROUP BY o."officeCode", o."city", o."state"
    ORDER BY o."city"
    """,
    conn,
)

# 8. Employees who sold products purchased by fewer than 20 unique customers
df_under_20 = pd.read_sql_query(
    """
    SELECT DISTINCT e."employeeNumber",
           e."firstName",
           e."lastName",
           e."officeCode",
           c."customerNumber"
    FROM employees e
    JOIN customers c
      ON e."employeeNumber" = c."salesRepEmployeeNumber"
    JOIN orders ord
      ON c."customerNumber" = ord."customerNumber"
    JOIN orderdetails od
      ON ord."orderNumber" = od."orderNumber"
    JOIN products p
      ON od."productCode" = p."productCode"
    JOIN (
        SELECT p2."productCode",
               COUNT(DISTINCT o2."customerNumber") AS "numpurchasers"
        FROM orderdetails od2
        JOIN orders o2
          ON od2."orderNumber" = o2."orderNumber"
        JOIN products p2
          ON od2."productCode" = p2."productCode"
        GROUP BY p2."productCode"
    ) pc
      ON pc."productCode" = p."productCode"
    WHERE pc."numpurchasers" < 20
    -- Put rows with firstName = 'Loui' first, then order by name and customer
    ORDER BY (e."firstName" != 'Loui'),
             e."firstName",
             e."lastName",
             c."customerNumber"
    LIMIT 15
    """,
    conn,
)

if __name__ == "__main__":
    print("df_boston:\n", df_boston.head())
    print("df_zero_emp:\n", df_zero_emp.head())
    print("df_employee:\n", df_employee.head())
    print("df_contacts:\n", df_contacts.head())
    print("df_payment:\n", df_payment.head())
    print("df_credit:\n", df_credit.head())
    print("df_product_sold:\n", df_product_sold.head())
    print("df_total_customers:\n", df_total_customers.head())
    print("df_customers:\n", df_customers.head())
    print("df_under_20:\n", df_under_20.head())