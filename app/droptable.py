from sqlalchemy import create_engine, text

# Define your database engine
engine = create_engine("sqlite:///database.db")

# Create a MetaData object bound to the engine
connection = engine.connect()

table_name = "comments"  # Replace 'comments' with the name of your table
drop_query = f"DROP TABLE IF EXISTS {table_name};"

# Execute the SQL query
connection.execute(text(drop_query))
connection.commit()
# Close the connection
connection.close()
