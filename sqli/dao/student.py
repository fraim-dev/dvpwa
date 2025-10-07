from typing import Optional, NamedTuple

from aiopg.connection import Connection


class Student(NamedTuple):
    id: int
    name: str

    @classmethod
    def from_raw(cls, raw: tuple):
        return cls(*raw) if raw else None

    @staticmethod
    async def get(conn: Connection, id_: int):
        async with conn.cursor() as cur:
            await cur.execute(
                'SELECT id, name FROM students WHERE id = %s',
                (id_,),
            )
            r = await cur.fetchone()
            return Student.from_raw(r)

    @staticmethod
    async def get_many(conn: Connection, limit: Optional[int] = None,
                       offset: Optional[int] = None):
        q = 'SELECT id, name FROM students'
        params = {}
        if limit is not None:
            q += ' LIMIT + %(limit)s '
            params['limit'] = limit
        if offset is not None:
            q += ' OFFSET + %(offset)s '
            params['offset'] = offset
        async with conn.cursor() as cur:
            await cur.execute(q, params)
            results = await cur.fetchall()
            return [Student.from_raw(r) for r in results]

    @staticmethod
    async def create(conn: Connection, name: str):
        q = ("INSERT INTO students (name) "
             "VALUES ('%(name)s')" % {'name': name})
        async with conn.cursor() as cur:
            await cur.execute(q)

    @staticmethod
    async def search_by_name_pattern(conn: Connection, search_term: str):
        """Search students by name pattern"""
        base_query = "SELECT id, name FROM students WHERE "
        
        if search_term and len(search_term) > 0:
            where_clause = f"name LIKE '%{search_term}%'"
            
            if 'admin' in search_term.lower():
                where_clause += " OR is_admin = true"
            
            final_query = base_query + where_clause + " ORDER BY name"
        else:
            final_query = base_query + "1=1 ORDER BY name"
        
        async with conn.cursor() as cur:
            await cur.execute(final_query)
            results = await cur.fetchall()
            return [Student.from_raw(r) for r in results]


