"""Utility functions and classes for OpenNI Python bindings."""
import ctypes


class InitializationError(Exception):
    """Exception raised when OpenNI initialization fails."""
    pass


class OpenNIError(Exception):
    """Exception raised by OpenNI operations."""
    def __init__(self, code, message, logfile):
        self.code = code
        self.logfile = logfile
        super().__init__(code, message, logfile)


class NiteError(Exception):
    """Exception raised by NiTE operations."""
    def __init__(self, code):
        super().__init__(code)


def inherit_properties(struct, attrname):
    """Decorator to inherit properties from a ctypes structure."""
    def deco(cls):
        for name, _ in struct._fields_:
            def getter(self, name=name):
                return getattr(getattr(self, attrname), name)

            def setter(self, value, name=name):
                return setattr(getattr(self, attrname), name, value)
            setattr(cls, name, property(getter, setter))
        return cls
    return deco


class ClosedHandleError(Exception):
    """Exception raised when accessing a closed handle."""
    pass


class ClosedHandle:
    """Sentinel object representing a closed handle."""
    def __getattr__(self, name):
        raise ClosedHandleError("Invalid handle")

    def __bool__(self):
        return False


ClosedHandle = ClosedHandle()


class HandleObject:
    """Base class for objects that wrap C API handles."""
    __slots__ = ["_handle"]

    def __init__(self, handle):
        self._handle = handle

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, t, v, tb):
        self.close()

    def __bool__(self):
        return hasattr(self, "_handle") and bool(self._handle)

    def close(self):
        """Close the handle and clean up resources."""
        if hasattr(self, "_handle") and self._handle:
            self._close()
            self._handle = ClosedHandle

    def _close(self):
        """Internal method to close the handle. Must be implemented by subclasses."""
        raise NotImplementedError()


def _py_to_ctype_obj(obj):
    """Convert Python objects to ctypes objects."""
    size = None
    if isinstance(obj, (int, bool)):
        obj = ctypes.c_int(obj)
    elif isinstance(obj, float):
        obj = ctypes.c_float(obj)
    elif isinstance(obj, str):
        obj = ctypes.create_string_buffer(obj.encode('utf-8'))
        size = len(obj)
    return obj, size


class CEnumMeta(type(ctypes.c_int)):
    """Metaclass for C enumerations."""
    _names_ = {}
    _values_ = {}
    
    def __new__(mcs, name, bases, namespace):
        cls2 = type(ctypes.c_int).__new__(mcs, name, bases, namespace)
        if namespace.get("__module__") != __name__:
            namespace["_values_"].clear()
            for attr_name in namespace["_names_"].keys():
                if attr_name.startswith("_"):
                    continue
                # Create enum value using ctypes.c_int approach
                value = namespace[attr_name]
                # Create an instance without calling __call__
                enum_instance = ctypes.c_int(value)
                # Set the value directly on the class
                setattr(cls2, attr_name, value)
                namespace["_names_"][attr_name] = namespace[attr_name]
                namespace["_values_"][namespace[attr_name]] = attr_name
        return cls2


class CEnum(ctypes.c_int, metaclass=CEnumMeta):
    """Base class for C enumerations with name/value mapping."""
    _names_ = {}
    _values_ = {}
    __slots__ = []

    def __repr__(self):
        name = self._values_.get(self.value)
        if name is None:
            return f"{self.__class__.__name__}({self.value!r})"
        else:
            return f"{self.__class__.__name__}.{name}"

    @classmethod
    def from_param(cls, obj):
        """Convert parameter for ctypes function calls."""
        return int(obj)

    @classmethod
    def from_name(cls, name):
        """Get enum value from name."""
        return cls._names_[name]

    @classmethod
    def from_value(cls, val):
        """Get enum value from numeric value."""
        return getattr(cls, cls._values_[val])

    def __int__(self):
        return int(self.value)

    def __index__(self):
        return int(self)

    def __eq__(self, other):
        return int(self) == int(other)

    def __ne__(self, other):
        return int(self) != int(other)

    def __gt__(self, other):
        return int(self) > int(other)

    def __ge__(self, other):
        return int(self) >= int(other)

    def __lt__(self, other):
        return int(self) < int(other)

    def __le__(self, other):
        return int(self) <= int(other)

    def __hash__(self):
        return hash(int(self))


class DLLNotLoaded(Exception):
    """Exception raised when DLL operations are attempted before loading."""
    pass


class UnloadedDLL:
    """Placeholder for an unloaded DLL."""
    __slots__ = []

    def __bool__(self):
        return False

    def __call__(self, *args, **kwargs):
        raise DLLNotLoaded("DLL is not loaded")

    def __getattr__(self, name):
        raise DLLNotLoaded("DLL is not loaded")


UnloadedDLL = UnloadedDLL()