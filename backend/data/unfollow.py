from data.connection import db_cursor
from data.users import User


def unfollow(follower: User, followee: User):
    with db_cursor() as cur:
        cur.execute(
            "DELETE FROM follows WHERE follower = %(follower_id)s AND followee = %(followee_id)s",
            dict(
                follower_id=follower.id,
                followee_id=followee.id,
            ),
        )
