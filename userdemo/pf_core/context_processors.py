
from . import _LOG

def pf_core(request):

    if hasattr(request, "pf_core_context"):
        pf_core = request.pf_core_context
        _LOG.debug('Adding pf_core structure: {}'.format(pf_core))

        if pf_core.get('sa_users', None):
            pf_core['sa_providers'] = [u.provider for u in pf_core['sa_users']]
        
    else:
        pf_core = {}
        _LOG.debug('Adding empty pf_core structure')
        
    return {
        "pf_core": pf_core,
    }
