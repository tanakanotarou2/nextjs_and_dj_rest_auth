from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class ApplicationAPIException(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_code = "application_error"

    def __init__(self, detail=None, code=None):
        """
        レスポンスのフォーマット変更したい場合は以下を参考に
        https://github.com/tanakanotarou2/dj-nextjs-poll-app/wiki/APIException-%E3%83%A1%E3%83%A2
        """
        super(ApplicationAPIException, self).__init__(detail, code)
