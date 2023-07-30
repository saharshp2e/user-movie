from cassandra.cluster import Cluster

# Connect to Cassandra running on localhost (127.0.0.1) with default port 9042
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('user_services')  # Replace 'user_services' with your actual keyspace

# Create a new table 'movie' with the correct schema
create_table_query = """
    CREATE TABLE IF NOT EXISTS movie (
        movie_id TEXT PRIMARY KEY,
        comments TEXT,
        users SET<TEXT>,
        users_who_commented SET<TEXT>
    )
"""
session.execute(create_table_query)

# Close the session and cluster
session.shutdown()
cluster.shutdown()
