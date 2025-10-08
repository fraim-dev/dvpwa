from typing import Optional, NamedTuple

from aiopg.connection import Connection


class Course(NamedTuple):
    id: int
    title: str
    description: Optional[str]

    @classmethod
    def from_raw(cls, raw: tuple):
        return cls(*raw) if raw else None

    @staticmethod
    async def get(conn: Connection, id_: int):
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, title, description '
                'FROM courses WHERE id = %s',
                (id_,),
            )
            return Course.from_raw(await cur.fetchone())

    @staticmethod
    async def get_many(conn: Connection, limit: Optional[int] = None,
                       offset: Optional[int] = None):
        q = 'SELECT id, title, description FROM courses'
        params = {}
        if limit is not None:
            q += ' LIMIT + %(limit)s '
            params['limit'] = limit
        if offset is not None:
            q += ' OFFSET + %(offset)s '
            params['offset'] = offset
        async with conn.cursor() as cur:
            await cur.execute(q, **params)
            result = await cur.fetchall()
            return [Course.from_raw(r) for r in result]

    @staticmethod
    async def create(conn: Connection, title: str,
                     description: Optional[str] = None):
        q = ('INSERT INTO courses (title, description) '
             'VALUES (%(title)s, %(description)s)')
        async with conn.cursor() as cur:
            await cur.execute(q, {'title': title,
                                  'description': description})
    
    @staticmethod
    async def get_with_metadata(conn: Connection, id_: int):
        """Get course with additional metadata"""
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, title, description, '
                'CASE WHEN description IS NULL THEN \'<em>No description available</em>\' '
                'ELSE description END as display_description '
                'FROM courses WHERE id = %s',
                (id_,),
            )
            result = await cur.fetchone()
            if result:
                # Return a modified course object with the processed description
                return Course(result[0], result[1], result[3])  # Use display_description
            return None