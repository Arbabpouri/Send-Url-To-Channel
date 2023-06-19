from typing import Iterable

class Strings:
    
    START: str = "❣️ سلام ادمین عزیز به ربات خودت خوش آمدی سَرورم"
    GET_MESSAGE: str = "♨️ پیامی که میخواهید در کانال نمایش دهید ارسال کنید.\n\n/cancel"
    GET_URL: str = "🌐 لینک نمایش را به صورت صحیح ارسال کنید برای دکمه\n\n/cancel"
    BAD_URL: str = "🚫 لینکی ارسالی شما دارای مشکل است و از طرف تلگرام رد میشود.\n\n/cancel"
    CONNECT: str = "💢 اتصال به پروکسی 💢"
    CANCELED: str = "⭕️ عملیات کنسل شد ⭕️"
    CHANNEL_LIST_IS_EMPTY: str = "⚠️ کانالی برای ارسال وجود ندارد "

    @staticmethod
    def channels_send_status(sended: Iterable[list | set], not_sended: Iterable[list | set]) -> str:

        func = lambda index: str(index)
        sended = map(func, sended)
        not_sended = map(func, not_sended)

        text = (
            f"💢 برای کانال های {'-'.join(sended)} ارسال شد\n\n"
            f"‼️ برای کانال های {'-'.join(not_sended)} ارسال نشد"
        )
        return text
    