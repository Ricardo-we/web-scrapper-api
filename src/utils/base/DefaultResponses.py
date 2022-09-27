
class DefaultResponses:
    @staticmethod
    def error_response(error: Exception, message: str = None):
        return {
            "error": error.__traceback__.__str__(),
            "message": message or error.__cause__.__str__()
        }

    @staticmethod
    def success_message(message="Success", status=200):
        return {
            "message": message
        }, status
