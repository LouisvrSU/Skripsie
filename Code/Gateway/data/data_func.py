########################################################################
# MAP
########################################################################
from gpx_converter import Converter

########################################################################
# Database
########################################################################

import sqlite3
import pandas as pd

########################################################################

def db_insert(sample_data):
    # Insert the sample data
    conn = sqlite3.connect('sample.db')

    # Create a cursor object
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO data (SN, Time, RSSI) VALUES (?, ?, ?)', sample_data)

    # Commit the changes and close the connection
    conn.commit()
    
    # Close the connection
    conn.close()
    
    print("Sample data inserted into the database from main.")


def db_setup():
    print("db setup")
    # Connect to the SQLite database (create it if it doesn't exist)
    conn = sqlite3.connect('sample.db')

    # Create a cursor object
    cursor = conn.cursor()

    # Create the 'data' table if it doesn't exist
    #(SN, sn_time, rssi_value, mod_state, rx_good)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data (
            SN INTEGER,
            Time TEXT,
            RSSI FLOAT
        )
    ''')
    print("data base has been set up!")
    
    # Close the database connection
    conn.close()
    
def db_init():

    # Connect to the SQLite database
    conn = sqlite3.connect('sample.db')

    # Query data from the database
    query = "SELECT * FROM data"

    # DATA BASE ERROR HANDELING
    #------------------------------------------------------------------------
    try:
        df1 = pd.read_sql(query, conn)
    except pd.errors.DatabaseError:
        print("ERROR")
        db_setup()
    finally:
        df1 = pd.read_sql(query, conn)
        return df1

    #------------------------------------------------------------------------
    
def db_update():
        # Connect to the SQLite database
    conn = sqlite3.connect('sample.db')

    # Query data from the database
    query = "SELECT * FROM data"

    # DATA BASE ERROR HANDELING
    #------------------------------------------------------------------------
    try:
        df1 = pd.read_sql(query, conn)
        df2 = pd.read_sql(query1, conn)
        print(df2)
    except pd.errors.DatabaseError:
        print("ERROR")
        db_setup()
    finally:
        df1 = pd.read_sql(query, conn)
        return df1  


########################################################################
# MAP
########################################################################

def read_map():
    # MAP DATA
    df_map = Converter(input_file='map.gpx').gpx_to_dataframe()
    return df_map