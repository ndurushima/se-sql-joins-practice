import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')


q = """
    SELECT * FROM employees
"""
print(pd.read_sql(q, conn))


# select names of all employees in Boston
q = """
    SELECT firstName, lastName
    FROM employees
    JOIN offices
        USING(officeCode)
    WHERE city = 'Boston';
"""
print(pd.read_sql(q, conn))


# Any office that have 0 employees?
q = """
    SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS n_employees
    FROM offices AS o
    LEFT JOIN employees AS e
    USING(officeCode)
    GROUP BY officeCode
    HAVING n_employees = 0
"""
print(pd.read_sql(q, conn))


# How many customers per office?
q = """
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
    FROM offices AS o
    JOIN employees AS e
        USING(officeCode)
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY officeCode
"""
print(pd.read_sql(q, conn))


# Display the names of every individual product that each employee has sold as a dataframe.
q = """
    SELECT firstName, lastName, productName
    FROM employees AS e
    JOIN customers AS c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders
        USING(customerNumber)
    JOIN orderdetails
        USING(orderNumber)
    JOIN products
        USING(productCode)
;
"""
print(pd.read_sql(q, conn))


# Display number of products each employee has sold, alpha last name, use quantityOrdered from orderDetails, what about same first or last name
q = """
SELECT firstName, lastName, SUM(quantityOrdered) as total_products_sold
FROM employees AS e
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders
    USING(customerNumber)
JOIN orderdetails
    USING(orderNumber)
GROUP BY firstName, lastName
ORDER BY lastName
;
"""
print(pd.read_sql(q, conn))


# Display the names of employees who have sold more than 200 different products.
q = """
SELECT firstName, lastName, COUNT(productCode) as different_products_sold
FROM employees AS e
JOIN customers AS c
    ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders
    USING(customerNumber)
JOIN orderdetails
    USING(orderNumber)
GROUP BY firstName, lastName
HAVING different_products_sold > 200
ORDER BY lastName
;
"""
print(pd.read_sql(q, conn))

conn.close()