from os.path import join, dirname
import setuptools

from packagetracker.version import __VERSION_STR__


def read(filename):
    return open(join(dirname(__file__), filename)).read()

setuptools.setup(
    name="packagetracker",
    version=__VERSION_STR__,
    description=(
        "Track packages from various package companies. "
        "See https://github.com/DJSymBiotiX/packagetracker for more."
    ),
    author="Fernando Chorney",
    author_email="github@djsbx.com",
    url="https://github.com/DJSymBiotiX/packagetracker",
    py_modules=['packagetracker'],
    license="GPL",
    keywords="track packages tracker ups fedex usps shipping",
    packages=setuptools.find_packages(exclude=['tests']),
    long_description=read("README.rst"),
    test_suite="nose.collector",
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python"
    ]
)
