from enum import IntEnum
from ctypes import (Structure, POINTER, CFUNCTYPE,
                    c_int, c_size_t, c_uint32, c_uint64, c_void_p, c_char_p)


__all__ = [
    # Designs
    "cxxrtl_toplevel",
    "cxxrtl_design_create_fn",
    # Design instances
    "cxxrtl_handle",
    "cxxrtl_create_fn", "cxxrtl_destroy_fn", "cxxrtl_step_fn",
    # Objects
    "cxxrtl_type",
    "cxxrtl_object", "cxxrtl_object_p",
    "cxxrtl_get_parts_fn", "cxxrtl_enum_fn"
    # VCD
    "cxxrtl_vcd",
    "cxxrtl_vcd_create_fn", "cxxrtl_vcd_destroy_fn",
    "cxxrtl_vcd_filter_fn", "cxxrtl_vcd_add_fn", "cxxrtl_vcd_add_from_fn",
    "cxxrtl_vcd_add_from_if_fn", "cxxrtl_vcd_add_from_without_memories_fn",
    "cxxrtl_vcd_sample_fn", "cxxrtl_vcd_read_fn",
]


class _cxxrtl_toplevel(Structure):
    pass


cxxrtl_toplevel = POINTER(_cxxrtl_toplevel)
cxxrtl_design_create_fn = CFUNCTYPE(cxxrtl_toplevel)


class _cxxrtl_handle(Structure):
    pass


cxxrtl_handle = POINTER(_cxxrtl_handle)
cxxrtl_create_fn = CFUNCTYPE(cxxrtl_handle, cxxrtl_toplevel)
cxxrtl_destroy_fn = CFUNCTYPE(None, cxxrtl_handle)
cxxrtl_step_fn = CFUNCTYPE(c_size_t, cxxrtl_handle)


class cxxrtl_type(IntEnum):
    VALUE  = 0
    WIRE   = 1
    MEMORY = 2
    ALIAS  = 3


class cxxrtl_object(Structure):
    _fields_ = [
        ("_type",   c_uint32),
        ("width",   c_size_t),
        ("lsb_at",  c_size_t),
        ("depth",   c_size_t),
        ("zero_at", c_size_t),
        ("curr",    POINTER(c_uint32)),
        ("next",    POINTER(c_uint32)),
    ]

    @property
    def type(self):
        return cxxrtl_type(self._type)

    @property
    def chunks(self):
        return ((self.width + 31) / 32) * self.depth


cxxrtl_object_p = POINTER(cxxrtl_object)
cxxrtl_get_parts_fn = CFUNCTYPE(cxxrtl_object_p, cxxrtl_handle, c_char_p, POINTER(c_size_t))
cxxrtl_enum_callback_fn = CFUNCTYPE(c_void_p, cxxrtl_object_p, c_size_t)
cxxrtl_enum_fn = CFUNCTYPE(None, cxxrtl_handle, c_void_p, cxxrtl_enum_callback_fn)


class _cxxrtl_vcd(Structure):
    pass


cxxrtl_vcd = POINTER(_cxxrtl_vcd)
cxxrtl_vcd_create_fn = CFUNCTYPE(cxxrtl_vcd)
cxxrtl_vcd_destroy_fn = CFUNCTYPE(None, cxxrtl_vcd)
cxxrtl_vcd_add_fn = CFUNCTYPE(cxxrtl_vcd, c_int, c_char_p);
cxxrtl_vcd_add_from_fn = CFUNCTYPE(cxxrtl_vcd, cxxrtl_handle)
cxxrtl_vcd_filter_fn = CFUNCTYPE(c_void_p, c_char_p, cxxrtl_object_p)
cxxrtl_vcd_add_from_if_fn = CFUNCTYPE(cxxrtl_vcd, cxxrtl_handle, c_void_p, cxxrtl_vcd_filter_fn)
cxxrtl_vcd_add_from_without_memories_fn = CFUNCTYPE(cxxrtl_vcd, cxxrtl_handle)
cxxrtl_vcd_sample_fn = CFUNCTYPE(cxxrtl_vcd, c_uint64)
cxxrtl_vcd_read_fn = CFUNCTYPE(cxxrtl_vcd, POINTER(c_char_p), POINTER(c_size_t))
