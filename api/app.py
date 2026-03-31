from flask import Flask, jsonify
from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')

engine = create_engine (f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')

app = Flask(__name__)



@app.route("/")
def home():
    return 'API is working!'



#total revenue
@app.route('/revenue')
def revenue():
    query = '''
            select sum(TotalPrice) as revenue
            from fact_sales
            '''
    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient='records'))



@app.route('/top-products')
def top_products():
    query = '''
            select d.Description , sum(f.TotalPrice) as revenue
            from fact_sales f
            join dim_product d
            on f.StockCode = d.StockCode
            group by d.Description
            order by revenue desc
            limit 10
            '''
    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient='records'))



@app.route('/top-customers')
def top_customers():
    query = '''
            select CustomerID , sum(TotalPrice) as revenue
            from fact_sales 
            group by CustomerID
            order by revenue desc
            limit 10
            '''
    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient='records'))



@app.route("/country-sales")
def country_sales():
    query = """
    SELECT c.Country, SUM(f.TotalPrice) AS revenue
    FROM fact_sales f
    JOIN dim_customer c ON f.CustomerID = c.CustomerID
    GROUP BY c.Country
    ORDER BY revenue DESC
    """
    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient="records"))



@app.route("/monthly-sales")
def monthly_sales():
    query = """
    SELECT d.Year, d.Month, SUM(f.TotalPrice) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.DateID = d.DateID
    GROUP BY d.Year, d.Month
    ORDER BY d.Year, d.Month
    """
    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True)