import uliweb
from uliweb.utils.setup import setup
import apps

__doc__ = """doc"""

setup(name='demo',
    version=apps.__version__,
    description="Description of your project",
    package_dir = {'demo':'apps'},
    packages = ['demo'],
    include_package_data=True,
    zip_safe=False,
)
