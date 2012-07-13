
class CookiePostHandlerMiddleware(object):
    """
    This middleware updates the response with additional cookies
    if the user is authenticated.

    This should be the last middleware you load.
    """
    def process_response(self, request, response):
        if request.user.is_authenticated():
            response.set_cookie('user_id', request.user.id)
        else:
            if request.COOKIES.has_key('user_id'):
                response.delete_cookie('user_id')
        return response
 
