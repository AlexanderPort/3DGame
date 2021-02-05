# python setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
import numpy


ext_modules = [
    Extension(
        "rasterization",
        ["rasterization.pyx"],
        extra_compile_args=['-O2', "-openmp"],
        extra_link_args=['-O2', "-openmp"],
        include_dirs=[numpy.get_include()]
    )
]

setup(
    name='rasterization',
    ext_modules=cythonize(ext_modules),
)
'''
setup(ext_modules=cythonize('rasterization.pyx'),
      include_dirs=[numpy.get_include()])
'''