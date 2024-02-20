from util import Database, RedisSession
from typing import Union, Tuple, Optional
from dtypes import Rating



class RatingsRepository:
    db_session: Database
    redis_session: RedisSession

    def __init__(self, db_session: Database, redis_session: RedisSession):
        self.db_session = db_session
        self.redis_session = redis_session

    
    def get_ratings_by_stay(self, stay_id: str) -> Tuple[bool, Union[str, Tuple[dict]]]:
        query = "SELECT * FROM ratings r JOIN stays s ON s.id = r.stay_id JOIN users u ON u.id = r.user_id WHERE r.stay_id = %s"
        success, err = self.db_session.execute_query(query, (stay_id,))
        if not success:
            return False, "An error has occurred"
        
        ratings = self.db_session.get_cursor().fetchall()
        if len(ratings) == 0:
            return False, "No Ratings Found"
        return True, tuple([Rating.from_tuple(rating).to_dict() for rating in ratings])
    
    def get_ratings_by_user(self, user_id: str) -> Tuple[bool, Union[str, Tuple[dict]]]:
        query = "SELECT * FROM ratings r JOIN stays s ON s.id = r.stay_id JOIN users u ON u.id = r.user_id WHERE r.user_id = %s"
        success, err = self.db_session.execute_query(query, (user_id,))
        if not success:
            return False, "An error has occurred"
        
        ratings = self.db_session.get_cursor().fetchall()
        if len(ratings) == 0:
            return False, "No Ratings Found"
        
        return True, tuple([Rating.from_tuple(rating).to_dict() for rating in ratings])
    
    def get_rating_by_id(self, rating_id: str) -> Tuple[bool, Union[str, dict]]:
        query = "SELECT * FROM ratings r JOIN stays s ON s.id = r.stay_id JOIN users u ON u.id = r.user_id WHERE r.id = %s"
        success, err = self.db_session.execute_query(query, (rating_id,))
        if not success:
            return False, "An error has occurred"
        
        rating = self.db_session.get_cursor().fetchone()
        if not rating:
            return False, "Rating Not Found"
        
        return True, Rating.from_tuple(rating).to_dict()
    
    def create_rating(self, user_id: str, stay_id: str, rating: float, title: str, comment: str) -> Tuple[bool, Optional[str]]:
        query = "INSERT INTO ratings (user_id, stay_id, rating, title, comment) VALUES (%s, %s, %s, %s, %s)"
        success, err = self.db_session.execute_query(query, (
                user_id,
                stay_id,
                rating,
                title,
                comment
            )
        )
        if not success:
            self.db_session.rollback()
            return False, err
        
        self.db_session.commit()
        return True, None
    
    def update_rating(self, rating_id: str, rating: Optional[float], title: Optional[str], comment: Optional[str]) -> Tuple[bool, Optional[str]]:
        all_query = "UPDATE ratings SET rating = %s, title = %s, comment = %s WHERE id = %s"
        title_query = "UPDATE ratings SET title = %s WHERE id = %s"
        comment_query = "UPDATE ratings SET comment = %s WHERE id = %s"
        rating_query = "UPDATE ratings SET rating = %s WHERE id = %s"

        if not rating and not title and not comment:
            return False, "No fields to update"
        
        query = all_query
        params = (rating, title, comment, rating_id)
        if rating and title and comment:
            query = all_query
            params = (rating, title, comment, rating_id)
        if not rating:
            query = rating_query
            params = (title, rating_id)
        elif not title:
            query = title_query
            params = (comment, rating_id)
        elif not comment:
            query = comment_query
            params = (comment, rating_id)



        success, err = self.db_session.execute_query(query, params)
        if not success:
            self.db_session.rollback()
            return False, err
        
        self.db_session.commit()
        return True, None
