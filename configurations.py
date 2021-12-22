
# URL
BASE_URL = 'https://www.nadlan.gov.il/'


# Table structure
COLUMNS = ['sale_date', 'Address', 'Gush', 'Type', 'Num_rooms', 'Floor', 'Size', 'Amount', 'Change']


# Scrolling Down
HOW_MANY_SCROLL_DOWN = 10
SLEEPING_TIME_BETWEEN_SCROLL = 5
HOW_MANY_PIXELS_SCROLL_DOWN = 2000


# Save csv

# Queries
# Create table
TABLE_NAME = 'property_sales'
QUERY_CREATE_TABLE = '''CREATE TABLE property_sales (
     sale_date DATE, 
     Address VARCHAR(100),
     Gush VARCHAR(100),
     Type VARCHAR(100),
     Num_rooms FLOAT,
     Floor VARCHAR(100),
     Size FLOAT,
     Amount FLOAT,
     Location VARCHAR,
     PRIMARY KEY (sale_date, Address, Gush, Location)
     );'''
# Insert data to db
COLUMNS_TO_INSERT = ['sale_date', 'Address', 'Gush', 'Type', 'Num_rooms', 'Floor', 'Size', 'Amount', 'Location']
INSERT_DATA = 'INSERT OR IGNORE INTO {0} {1} VALUES {2};'
