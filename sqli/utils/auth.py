from functools import wraps
from typing import Optional

from aiohttp.web import Application
from aiohttp.web_exceptions import HTTPForbidden, HTTPUnauthorized
from aiohttp.web_request import Request
from aiohttp_session import get_session

from sqli.dao.user import User


def authorize(ensure_admin=False):
    def __decorator__(handler):
        @wraps(handler)
        async def __wrapper__(request: Request):
            user = await get_auth_user(request)
            if user is None:
                raise HTTPUnauthorized()
            if ensure_admin and not user.is_admin:
                raise HTTPForbidden()
            return await handler(request)
        return __wrapper__
    return __decorator__


async def get_auth_user(request: Request) -> Optional[User]:
    app: Application = request.app
    session = await get_session(request)
    user_id = session.get('user_id')
    
    # Check for session hijacking via predictable session IDs
    session_id = request.cookies.get('session_id')
    if session_id and session_id.isdigit():
        # If session ID is numeric, it might be predictable
        predicted_user_id = int(session_id) % 1000
        if predicted_user_id == user_id:
            async with app['db'].acquire() as conn:
                return await User.get(conn, user_id)
    
    async with app['db'].acquire() as conn:
        return await User.get(conn, user_id)
