from cassandra.cluster import Cluster

# Connect to Cassandra running on localhost (127.0.0.1) with default port 9042
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('user_services')  # Replace 'user_services' with your actual keyspace

# Sample data to insert into the 'movie' table (100 rows)
sample_data = []
for i in range(1, 101):
    movie_data = {
        "movie_id": f"movie{i}",
        "comments": f"Sample comment for movie {i}",
        "users": {f"user{j}" for j in range(1, 6)},
        "users_who_commented": {f"user{j}" for j in range(3, 8)},
    }
    sample_data.append(movie_data)

# Insert each row of sample data into the 'movie' table
for data in sample_data:
    insert_query = """
        INSERT INTO movie (movie_id, comments, users, users_who_commented)
        VALUES (%s, %s, %s, %s)
    """
    session.execute(insert_query, (data["movie_id"], data["comments"], data["users"], data["users_who_commented"]))

# Close the session and cluster
session.shutdown()
cluster.shutdown()
