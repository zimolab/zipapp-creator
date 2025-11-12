class _Messages(object):
    def __init__(self):
        from .common import trfunc

        tr = trfunc()


_messages = None


def messages() -> _Messages:
    global _messages
    if _messages is None:
        _messages = _Messages()
    return _messages
