from typing import Optional


class ApplicationException(Exception):
    """アプリケーションで発生させる例外のベースクラス"""

    message = "不明なエラーが発生しました。"

    def __init__(self, message: Optional[str] = None, *args, **kwargs):
        if message:
            self.message = message
        super(ApplicationException, self).__init__(*args)
