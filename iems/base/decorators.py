from functools import wraps
from inspect import isawaitable
from typing import Any, Optional

from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails
from sanic import Request

from iems.base.models import DataValidationExceptionModel, ValidationError as ErrorModel
from iems.base.response import JSONResponse


def __pydantic_validate_data(
    model: BaseModel, data: dict[Any, Any]
) -> BaseModel | list[ErrorDetails]:
    try:
        model.model_json_schema()
        return model.model_validate(data)
    except ValidationError as error:
        return error.errors(include_url=False, include_input=False)


def __pydantic_validate_json(
    model: BaseModel, data: str
) -> BaseModel | list[ErrorDetails]:
    try:
        return model.model_validate_json(data)
    except ValidationError as error:
        return error.errors(include_url=False, include_input=False)


def validate(
    body: Optional[BaseModel] = None,
    query: Optional[BaseModel] = None,
    path: Optional[BaseModel] = None,
):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            errors = []
            query_params = None
            path_params = None
            data = None
            if query is not None and issubclass(query, BaseModel):
                print(request.get_args(keep_blank_values=True, strict_parsing=True))
                result = __pydantic_validate_data(
                    query, request.get_args(keep_blank_values=True, strict_parsing=True)
                )
                if isinstance(result, BaseModel):
                    query_params = result
                else:
                    errors.extend(result)
            if path is not None and issubclass(path, BaseModel):
                result = __pydantic_validate_data(path, kwargs)
                if isinstance(result, BaseModel):
                    path_params = result
                else:
                    errors.extend(result)
            if body is not None and issubclass(body, BaseModel):
                result = __pydantic_validate_json(body, request.body)
                if isinstance(result, BaseModel):
                    data = result
                else:
                    errors.extend(result)
            if len(errors) != 0:
                errors = [
                    ErrorModel.model_construct(
                        type=error["type"], location=list(error["loc"])
                    )
                    for error in errors
                ]
                return JSONResponse(
                    DataValidationExceptionModel.model_construct(
                        context=errors
                    ).model_dump_json(),
                    422,
                )
            response = f(
                request,
                query_params=query_params,
                path_params=path_params,
                data=data,
                *args,
                **kwargs,
            )
            if isawaitable(response):
                response = await response
            return response

        return decorated_function

    return decorator
