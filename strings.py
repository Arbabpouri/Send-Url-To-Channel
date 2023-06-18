from typing import Iterable

class Strings:
    
    START = "a"
    GET_MESSAGE = "b"
    GET_URL = "c"
    BAD_URL = "d"
    BAD_MESSAGE = "e"
    CONNECT = "f"
    CANCELED = "g"
    CHANNEL_LIST_IS_EMPTY = "ss"

    @staticmethod
    def channels_send_status(sended: Iterable[list | set], not_sended: Iterable[list | set]) -> str:

        func = lambda index: str(index)
        sended = map(func, sended)
        not_sended = map(func, not_sended)

        text = (
            f"s : {'-'.join(sended)}"
            "\n\n"
            f"n : {'-'.join(not_sended)}"
        )
        return text
    