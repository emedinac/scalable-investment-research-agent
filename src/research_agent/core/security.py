from fastapi import Request


def get_user_id(request: Request) -> str:
    return request.headers.get("x-user-id", "anonymous")
