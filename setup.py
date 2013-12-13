__doc__ = """
Uliweb-Admin
"""

from uliweb.utils.setup import setup
import uliweb_admin

setup(name='uliweb_admin',
    version=uliweb_admin.__version__,
    description="Admin app for uliweb",
    long_description=__doc__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ],
    packages = ['uliweb_admin'],
    platforms = 'any',
    keywords='uliweb app',
    author=uliweb_admin.__author__,
    author_email=uliweb_admin.__author_email__,
    url=uliweb_admin.__url__,
    license=uliweb_admin.__license__,
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'uliweb_apps': [
          'helpers = uliweb_admin',
        ],
    },
)
