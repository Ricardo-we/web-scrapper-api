
class DefaultResponses:
    @staticmethod
    def error_response(error: Exception, message: str):
        return {
            "error": str(error),
            "message": message
        }
    
    @staticmethod
    def success_message(message="Success", status=200):
        return {
            "message": message
        }, status
