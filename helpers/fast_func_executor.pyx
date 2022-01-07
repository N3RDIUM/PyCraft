cdef fast_exec_(func):
    cdef _func = func
    _func()

def fast_exec(func):
    fast_exec_(func)
