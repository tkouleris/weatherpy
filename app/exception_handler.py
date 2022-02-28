from app import app
from app.exceptions import UnauthenticatedException, ResourceNotFoundException


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, UnauthenticatedException):
        return {"success": "false", "error": e.message}, e.status_code

    if isinstance(e, ResourceNotFoundException):
        return {"success": "false", "error": e.message}, e.status_code