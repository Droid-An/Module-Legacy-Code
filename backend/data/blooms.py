import datetime

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from data.connection import db_cursor
from data.users import User


@dataclass
class Bloom:
    id: int
    sender: User
    content: str
    sent_timestamp: datetime.datetime
    reblooms: int
    original_bloom_id: int


def add_bloom(
    *, sender: User, content: str, original_bloom_id: Optional[int] = None
) -> Bloom:
    hashtags = [word[1:] for word in content.split(" ") if word.startswith("#")]

    now = datetime.datetime.now(tz=datetime.UTC)
    bloom_id = int(now.timestamp() * 1000000)
    print(original_bloom_id)
    with db_cursor() as cur:
        cur.execute(
            "INSERT INTO blooms (id, sender_id, content, send_timestamp, reblooms, original_bloom_id) VALUES (%(bloom_id)s, %(sender_id)s, %(content)s, %(timestamp)s, %(reblooms)s,%(original_bloom_id)s)",
            dict(
                bloom_id=bloom_id,
                sender_id=sender.id,
                content=content,
                timestamp=datetime.datetime.now(datetime.UTC),
                reblooms=0,
                original_bloom_id=original_bloom_id,
            ),
        )
        for hashtag in hashtags:
            cur.execute(
                "INSERT INTO hashtags (hashtag, bloom_id) VALUES (%(hashtag)s, %(bloom_id)s)",
                dict(hashtag=hashtag, bloom_id=bloom_id),
            )


def get_blooms_for_user(
    username: str, *, before: Optional[int] = None, limit: Optional[int] = None
) -> List[Bloom]:
    with db_cursor() as cur:
        kwargs = {
            "sender_username": username,
        }
        if before is not None:
            before_clause = "AND send_timestamp < %(before_limit)s"
            kwargs["before_limit"] = before
        else:
            before_clause = ""

        limit_clause = make_limit_clause(limit, kwargs)

        cur.execute(
            f"""SELECT
                blooms.id,
                users.username,
                blooms.content,
                blooms.send_timestamp,
                COALESCE(reblooms.reblooms, 0) AS reblooms,
                blooms.original_bloom_id
            FROM blooms
            INNER JOIN users ON users.id = blooms.sender_id
            LEFT JOIN (
                SELECT
                    original_bloom_id,
                    COUNT(*) AS reblooms
                FROM blooms
                WHERE original_bloom_id IS NOT NULL
                GROUP BY original_bloom_id
            ) as reblooms ON reblooms.original_bloom_id = blooms.id
            WHERE
              username = %(sender_username)s
              {before_clause}
            ORDER BY send_timestamp DESC
            {limit_clause}
            """,
            kwargs,
        )
        rows = cur.fetchall()
        blooms = []
        for row in rows:
            (
                bloom_id,
                sender_username,
                content,
                timestamp,
                reblooms,
                original_bloom_id,
            ) = row
            blooms.append(
                Bloom(
                    id=bloom_id,
                    sender=sender_username,
                    content=content,
                    sent_timestamp=timestamp,
                    reblooms=reblooms,
                    original_bloom_id=original_bloom_id,
                )
            )
    return blooms


def get_bloom(bloom_id: int) -> Optional[Bloom]:
    with db_cursor() as cur:
        cur.execute(
            """SELECT
	BLOOMS.ID,
	USERS.USERNAME,
	CONTENT,
	SEND_TIMESTAMP,
	COALESCE(reblooms.reblooms, 0) AS reblooms,
	blooms.ORIGINAL_BLOOM_ID
FROM
	BLOOMS
INNER JOIN USERS ON
	USERS.ID = BLOOMS.SENDER_ID
LEFT JOIN (
	SELECT
		ORIGINAL_BLOOM_ID,
		COUNT(*) AS REBLOOMS
	FROM
		BLOOMS
	WHERE
		ORIGINAL_BLOOM_ID IS NOT NULL
	GROUP BY
		ORIGINAL_BLOOM_ID
            ) AS REBLOOMS ON
	REBLOOMS.ORIGINAL_BLOOM_ID = BLOOMS.ID
WHERE
	BLOOMS.ID = %s""",
            (bloom_id,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        bloom_id, sender_username, content, timestamp, reblooms, original_bloom_id = row
        return Bloom(
            id=bloom_id,
            sender=sender_username,
            content=content,
            sent_timestamp=timestamp,
            reblooms=reblooms,
            original_bloom_id=original_bloom_id,
        )


def get_blooms_with_hashtag(
    hashtag_without_leading_hash: str, *, limit: int = None
) -> List[Bloom]:
    kwargs = {
        "hashtag_without_leading_hash": hashtag_without_leading_hash,
    }
    limit_clause = make_limit_clause(limit, kwargs)
    with db_cursor() as cur:
        cur.execute(
            f"""select
	blooms.id,
	users.username,
	blooms.content,
	blooms.send_timestamp,
	coalesce(reblooms.reblooms, 0) as reblooms,
	blooms.original_bloom_id
from
	blooms
inner join hashtags on
	blooms.id = hashtags.bloom_id
inner join users on
	blooms.sender_id = users.id
left join (
	select
		original_bloom_id,
		COUNT(*) as reblooms
	from
		blooms
	where
		original_bloom_id is not null
	group by
		original_bloom_id
            ) as reblooms on
	reblooms.original_bloom_id = blooms.id
            WHERE
              hashtag = %(hashtag_without_leading_hash)s
            ORDER BY send_timestamp DESC
            {limit_clause}
            """,
            kwargs,
        )
        rows = cur.fetchall()
        blooms = []
        for row in rows:
            (
                bloom_id,
                sender_username,
                content,
                timestamp,
                reblooms,
                original_bloom_id,
            ) = row
            blooms.append(
                Bloom(
                    id=bloom_id,
                    sender=sender_username,
                    content=content,
                    sent_timestamp=timestamp,
                    reblooms=reblooms,
                    original_bloom_id=original_bloom_id,
                )
            )
    return blooms


# remove when remove rebloom column from db
def update_rebloom_counter(bloom_id: int) -> None:
    with db_cursor() as cur:
        cur.execute(
            "UPDATE blooms SET reblooms = reblooms + 1 WHERE blooms.id = %s",
            (bloom_id,),
        )


def add_rebloom(*, sender: User, id: int) -> None:
    original_bloom = get_bloom(id)
    if not original_bloom:
        return None
    content = original_bloom.content
    # remove, because you don't have to update column I delete
    update_rebloom_counter(id)
    add_bloom(sender=sender, content=content, original_bloom_id=id)


def make_limit_clause(limit: Optional[int], kwargs: Dict[Any, Any]) -> str:
    if limit is not None:
        limit_clause = "LIMIT %(limit)s"
        kwargs["limit"] = limit
    else:
        limit_clause = ""
    return limit_clause
