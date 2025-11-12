-- Load sample data into ClimateControl table.
INSERT INTO ClimateControl (ClimateControlled, MonthlyRate) VALUES
    (TRUE, 500.00),
    (FALSE, 400.00);

-- Load sample data into Customer table.
INSERT INTO Customer (ID, FirstName, LastName, Phone, Email, Address) VALUES
    (1, 'Alice', 'Anderson', '555-1234', 'alice@example.com', '123 Main St'),
    (2, 'Bob', 'Brown', '555-2345', 'bob@example.com', '456 Oak Ave'),
    (3, 'Charlie', 'Clark', '555-3456', 'charlie@example.com', '789 Pine Rd');

-- Load sample data into StorageUnit table.
INSERT INTO StorageUnit (ID, Floor, ClimateControlled) VALUES
    (101, 1, TRUE),
    (102, 2, FALSE),
    (103, 1, TRUE);

-- Load sample data into RentalContract table.
INSERT INTO RentalContract (ID, StartDate, EndDate, MonthlyRate, Customer_ID, Unit_ID) VALUES
    (1001, '2025-01-01', '2025-06-30', 500.00, 1, 101),
    (1002, '2025-02-15', '2025-07-15', 400.00, 2, 102),
    (1003, '2025-03-01', '2025-09-01', 500.00, 3, 103);

-- Load sample data into Payment table.
INSERT INTO Payment (ID, PaymentDate, Amount, Method, Contract_ID) VALUES
    (2001, '2025-01-01', 500.00, 'Credit Card', 1001),
    (2002, '2025-02-01', 500.00, 'Cash', 1001),
    (2003, '2025-02-15', 400.00, 'Credit Card', 1002),
    (2004, '2025-03-01', 500.00, 'Bank Transfer', 1003);
