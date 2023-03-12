class HTTPException(Exception):
    """Вызывается при несоответствии HTTP-кода с ожидаемым."""

    ...


class MissedKeyException(Exception):
    """Вызывается при отсутствии ожидаемого ключа в словаре."""

    ...


class WrongDataFormat(Exception):
    """Вызывается при несоответствии типа полученных данных с ожидаемым."""

    ...
