from typing import List, Optional


class Rating:
    id: str
    user_id: str
    customer_name: str
    stay_id: str
    stay_name: str
    rating: float
    title: str
    review: str
    created_at: Optional[str]
    updated_at: Optional[str]

    def __init__(self):
        self.id = ""
        self.user_id = ""
        self.customer_name = ""
        self.stay_id = ""
        self.stay_name = ""
        self.rating = 0
        self.title = ""
        self.review = ""
        self.created_at = None
        self.updated_at = None

    @staticmethod
    def from_tuple(rating_tuple: tuple):
        rating = Rating()
        rating.id = rating_tuple[0]
        rating.user_id = rating_tuple[1]
        rating.stay_id = rating_tuple[2]
        rating.rating = rating_tuple[3]
        rating.title = rating_tuple[4]
        rating.review = rating_tuple[5]
        rating.created_at = rating_tuple[6]
        rating.updated_at = rating_tuple[7]
        rating.stay_name = rating_tuple[11]
        rating.customer_name = f"{rating_tuple[26]} {rating_tuple[27]}"
        return rating

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "stay_id": self.stay_id,
            "rating": self.rating,
            "title": self.title,
            "review": self.review,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
