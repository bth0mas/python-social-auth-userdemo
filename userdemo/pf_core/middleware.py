
from social_django.models import UserSocialAuth

from . import _LOG

from  .models         import PfUser


## TODO rename this

class PfCoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        ## ------------------------------------------------------------
        ## Code to be executed for each request before
        ## the view (and later middleware) are called.
        ##

        # _LOG.debug('Request: ({}) {}'.format(type(request), dir(request)))
        # _LOG.debug('Session: ({}) {}'.format(type(request.session),
        #                                      dir(request.session)))
        
        user = getattr(request, 'user', None)

        if user is not None and user.is_authenticated:
            _LOG.debug('found user: {} ({} // {})'
                       .format(user, type(user), repr(user)))

            sa_users = UserSocialAuth.objects.filter(user=user)
            
            request.pf_core_context = {'sa_users': sa_users}
        else:
            _LOG.debug('not authenticated')
            # request.calsync_context['user'] = {'is_authenticated': False}
        
        ## ------------------------------------------------------------
        ##  central action
        ##
        response = self.get_response(request)

        ## ------------------------------------------------------------
        ## Code to be executed for each request/response after
        ## the view is called.


        ## ------------------------------------------------------------
        ## And don't forget to return the response...
        ##
        return response

