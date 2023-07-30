from .models import MovieComment
from .database import CassandraDB
from .redis_cache import RedisCache
import json

db = CassandraDB(['127.0.0.1'], 'user_services')  # Replace 'your_cassandra_host' and 'your_keyspace' with actual values
cache = RedisCache('127.0.0.1', 6379, 0)  # Replace 'your_redis_host' with your actual Redis host



def serialize_sorted_set(sorted_set):
    return list(sorted_set)

def row_to_dict(row, column_names):
    return dict(zip(column_names, row))


# Object-oriented approach for managing comments
class MovieCommentManager:
    def create_comment(self, comment: MovieComment):
        query = """
            INSERT INTO movie (movie_id, users, comments, users_who_commented)
            VALUES (%s, %s, %s, %s)
        """
        db.execute_query(query, (comment.movie_id, comment.users, comment.comments, comment.users_who_commented))
        cache.delete(f"movie_comments:{comment.movie_id}")  # Delete cache to ensure data consistency


    def get_comments_by_movie_id(self, movie_id: str):
        cached_comments = cache.get(f"movie:{movie_id}")
        if cached_comments:
            print('coming from redis cache')
            comments_list = json.loads(cached_comments)  # Convert the string back to a list of dictionaries
            for comment in comments_list:
                # Convert SortedSet objects to lists before returning
                comment['users'] = serialize_sorted_set(comment['users'])
                comment['users_who_commented'] = serialize_sorted_set(comment['users_who_commented'])
                for key, value in comment.items():
                    print(f"{key}: {value}")
            return comments_list

        else:
            query = """
                SELECT movie_id, comments, users, users_who_commented FROM movie WHERE movie_id=%s
            """
            rows = db.execute_query(query, (movie_id,))
            column_names = ["movie_id", "comments", "users", "users_who_commented"]  # Column names in the same order as they appear in the tuple
            comments = []
            for row in rows:
                row_dict = row_to_dict(row, column_names)  # Convert the tuple to a dictionary
                row_dict['users'] = serialize_sorted_set(row_dict['users'])
                row_dict['users_who_commented'] = serialize_sorted_set(row_dict['users_who_commented'])
                comments.append(row_dict)
            cache.setex(f"movie:{movie_id}", 60 , json.dumps(comments))
            print('added to redis cache')
            return comments
        
    def get_comments_for_user(self, movie_id: str, user: str):
        comments = self.get_comments_by_movie_id(movie_id)
        user_comments = [comment for comment in comments if user in comment['users']]
        return user_comments