
from pprint import pprint, pformat


def _pprint(o, lmargin=0, width=80, **kwargs):

    w = width - lmargin

    s = pformat(o, width=w, **kwargs)

    for l in s.split("\n"):
        print('{}{}'.format(' ' * lmargin, l))

        

def debug(response, details, *args, **kwargs):
    
    print("#" * 80)

    print('    ## response')
    _pprint(response, lmargin=4)
    
    print(" " * 4 + '##' + "-" * 72)
    print('    ## details')
    _pprint(details, lmargin=4)
    
    print(" " * 4 + '##' + "-" * 72)
    print('    ## args')
    _pprint(args, lmargin=4)
    
    print(" " * 4 + '##' + "-" * 72)
    print('    ## kwargs')
    _pprint(kwargs, lmargin=4)
    
    print("#" * 80)
