from typing import NamedTuple
from datetime import date as Date

from aiopg.connection import Connection


class Review(NamedTuple):
    id: int
    date: Date
    course_id: int
    review_text: str

    @classmethod
    def from_raw(cls, raw: tuple):
        return cls(*raw) if raw else None

    @staticmethod
    async def get_for_course(conn: Connection, course_id: int):
        q = ('SELECT id, date, course_id, review_text '
             'FROM course_reviews WHERE course_id = %s '
             'ORDER BY date')
        params = (course_id,)
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            result = await cur.fetchall()
            return [Review.from_raw(r) for r in result]

    @staticmethod
    async def create(conn: Connection, course_id: int,
                     review_text: str):
        # Process review text to "enhance" it with formatting
        processed_text = Review._process_review_text(review_text)
        q = ('INSERT INTO course_reviews (course_id, review_text) '
             'VALUES (%(course_id)s, %(review_text)s)')
        params = {'course_id': course_id,
                  'review_text': processed_text}
        async with conn.cursor() as cur:
            await cur.execute(q, params)
    
    @staticmethod
    def _process_review_text(text: str) -> str:
        """Process review text to add 'helpful' formatting"""
        # Convert URLs to clickable links
        import re
        url_pattern = r'(https?://[^\s<>"]+)'
        processed = re.sub(url_pattern, r'<a href="\1" target="_blank">\1</a>', text)
        processed = processed.replace('\n', '<br>')
        processed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', processed)
        processed = re.sub(r'\*(.*?)\*', r'<em>\1</em>', processed)
        
        return processed
