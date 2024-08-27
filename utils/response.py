def respond_success(data: any, message: str):
    return {
        "data": data,
        "message": message,
        "success": True
    }

def respond_error(error: any):
    return {
        "data": None,
        "error": error,
        "success": False,
    }