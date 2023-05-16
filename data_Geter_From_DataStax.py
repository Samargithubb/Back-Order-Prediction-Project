import pandas as pd
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os

secure_connect_database = os.getenv("Secure-Connect-Database")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET_KEY = os.getenv("CLIENT-SECRET-KEY")

cloud_config = {
    'secure_connect_bundle': secure_connect_database
}
auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET_KEY)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect('backorderprediction')
# Execute a SELECT query to retrieve the data
query = 'SELECT * FROM train_data'
rows = session.execute(query)

# Convert the data to a pandas DataFrame
df = pd.DataFrame(rows)

# Create the directory if it doesn't exist
if not os.path.exists('Training_FileFromDB'):
    os.makedirs('Training_FileFromDB')


# Save the data to a CSV file
df.to_csv('Training_FileFromDB/train_data.csv', index=False)
