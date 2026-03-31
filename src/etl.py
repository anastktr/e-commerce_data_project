import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv



df = pd.read_csv(r'C:\Users\anast\Desktop\E-Commerce\Data\Raw_Data\data.csv', encoding="ISO-8859-1")


df = df[~df['InvoiceNo'].str.contains('C')]

df = df.drop_duplicates()

df = df[df['Quantity'] > 0]

df = df[~df['CustomerID'].isna()]

df = df[~df['Country'].isin(['Unspecified'])]

df = df[df['UnitPrice'] > 0]

special_codes = ['M', 'POST', 'BANK CHARGES', 'DOT', 'C2', 'PADS']
df = df[~df['StockCode'].isin(special_codes)]

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['InvoiceDATE'] = df['InvoiceDate'].dt.date
df['Time'] = df['InvoiceDate'].dt.time
df.drop(columns='InvoiceDate', inplace=True)

df['Quantity'] = df['Quantity'].astype(int)
df['UnitPrice'] = df['UnitPrice'].astype(float)
df['UnitPrice'] = df['UnitPrice'].astype(float)
df['StockCode'] = df['StockCode'].astype(str).str.strip()
df['CustomerID'] = df['CustomerID'].astype(int)
df['InvoiceDATE'] = pd.to_datetime(df['InvoiceDATE'])

#df.to_csv('done5.csv', index=False)



dim_customer = df[['CustomerID','Country']].drop_duplicates()
dim_customer = dim_customer.drop_duplicates(subset=['CustomerID'])

dim_product = df[['StockCode','Description']].drop_duplicates()
dim_product.drop_duplicates(subset='StockCode',inplace=True)

dim_date = df[['InvoiceDATE']].drop_duplicates().copy()
dim_date['DateID'] = dim_date['InvoiceDATE'].dt.strftime('%Y%m%d').astype(int).drop_duplicates()
dim_date['Year'] = dim_date['InvoiceDATE'].dt.year
dim_date['Month'] = dim_date['InvoiceDATE'].dt.month
dim_date['Day'] = dim_date['InvoiceDATE'].dt.day
dim_date['Weekday'] = dim_date['InvoiceDATE'].dt.weekday



fact_table = df.merge(dim_date[['InvoiceDATE', 'DateID']], on='InvoiceDATE', how='left')
fact_table['TotalPrice'] = fact_table['Quantity'] * fact_table['UnitPrice']
fact_table = fact_table[['InvoiceNo','DateID','CustomerID','StockCode','Quantity','UnitPrice','TotalPrice']]
fact_table = fact_table.drop_duplicates(subset=['InvoiceNo','StockCode'])

dim_customer.to_csv('customer.csv', index=False)
dim_product.to_csv('product.csv', index=False)
dim_date.to_csv('date.csv', index=False)
fact_table.to_csv('fact.csv', index=False)




#load environmental variables
load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")


engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")


dim_customer.to_sql('dim_customer', con=engine, if_exists='append', index=False)
dim_product.to_sql('dim_product', con=engine, if_exists='append', index=False)
dim_date.to_sql('dim_date', con=engine, if_exists='append', index=False)
fact_table.to_sql('fact_sales', con=engine, if_exists='append', index=False)
