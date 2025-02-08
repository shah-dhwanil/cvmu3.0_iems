from sanic.response import HTTPResponse


def JSONResponse(body: str, status_code: int, **kwargs):
    return HTTPResponse(body, status_code, content_type="application/json", **kwargs)
