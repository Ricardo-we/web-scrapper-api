
class DefaultResponses:
    @staticmethod
    def error_response(error: Exception, message: str = None):
        return {
            "error": error.__class__.__name__,
            "message": message or error.args[0]
        }

    @staticmethod
    def success_message(message="Success", status=200):
        return {
            "message": message
        }, status
