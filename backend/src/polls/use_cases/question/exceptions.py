from lib.interfaces.application.exceptions import ApplicationException


class VotePeriodException(ApplicationException):
    message = "現在この質問には投票できません"
