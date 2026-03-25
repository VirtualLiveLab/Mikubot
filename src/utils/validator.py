from typing import Any, TypeIs, TypeVar

T = TypeVar("T", bound=Any)


def validate[T: Any](var: Any, expected_type: type[T]) -> TypeIs[T]:  # noqa: ANN401
    if isinstance(var, expected_type):
        return var
    msg = f"{var} is not a {expected_type}"
    raise TypeError(msg)
