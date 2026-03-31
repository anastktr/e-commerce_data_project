CREATE DATABASE IF NOT EXISTS ECommerce_db;
USE ECommerce_db;


CREATE TABLE dim_customer (
	CustomerID INT PRIMARY KEY,
    Country VARCHAR(50)
);


CREATE TABLE dim_product (
	StockCode VARCHAR(20) PRIMARY KEY,
    `Description` VARCHAR(255)
);


CREATE TABLE dim_date (
    DateID INT PRIMARY KEY,
    `Date` DATE,
    `Year` INT,
    `Month` INT,
    `Day` INT,
    Weekday INT
);


CREATE TABLE fact_sales(
    InvoiceNo VARCHAR(20),
    DateID INT,
    CustomerID INT,
    StockCode VARCHAR(20),
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    TotalPrice DECIMAL(12,2),
    PRIMARY KEY (InvoiceNo, StockCode),
    FOREIGN KEY (DateID) REFERENCES dim_date(DateID),
    FOREIGN KEY (CustomerID) REFERENCES dim_customer(CustomerID),
    FOREIGN KEY (StockCode) REFERENCES dim_product(StockCode)
);


