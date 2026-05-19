#!/usr/bin/env python
"""OpenNI2 and NiTE2 Python bindings setup configuration."""

from setuptools import setup

setup(
    name="openni-python3",
    version="2.4.0",
    description="OpenNI2 and NiTE2 Python bindings",
    author="PrimeSense Inc, Séverin Lemaignan, Jerome Flesch, Hajime Murao, Graoui Abderrahmane",
    author_email="primesense.com, severin.lemaignan@brl.ac.uk, graoui.abderrahmane2002@gmail.com",
    license="MIT",
    url="https://github.com/MerGr/openni-python3",
    packages=["openni"],
    platforms=["POSIX", "Windows"],
    python_requires=">=3.8",
    keywords="PrimeSense, OpenNI, OpenNI2, Natural Interaction, NiTE, NiTE2",
    long_description="""\
Python-bindings for `OpenNI2 <https://github.com/OpenNI/OpenNI2>`_
and `NiTE2 <http://openni.ru/files/nite/>`_.

This package provides only the Python bindings; be sure to install OpenNI2 (and optionally NiTE2) first.

Example::
    
    from openni import openni2
    
    openni2.initialize()     # can also accept the path of the OpenNI redistribution
    
    dev = openni2.Device.open_any()
    print(dev.get_device_info())
    
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    depth_stream.stop()
    
    openni2.unload()


.. note:: Refer to the OpenNI2/NiTE2 C API for complete documentation

""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
)

