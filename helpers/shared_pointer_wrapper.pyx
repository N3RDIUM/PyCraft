from cython.operator cimport dereference as deref
from libcpp.memory cimport shared_ptr, make_shared

cdef class SharedManager:
    cdef public shared_ptr[SharedManager] self

    def __cinit__(self):
        self.sharedIndexes = []
    
    cdef _setter(self, value):
        cdef _ = value
        cdef ptr = make_shared[SharedManager](_)
        self.sharedIndexes.append(ptr)
    
    cdef _getter(self, index):
        return deref(index)

    def getter(self, index):
        return self._getter(index)
    
    def setter(self, value):
        return self._setter(value)

def make_shared_pointer():
    return SharedManager()
