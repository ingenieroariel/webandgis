import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.md')).read()
README += '\n\n'
README += open(os.path.join(here, 'CHANGES')).read()


setup(
    name='webandgis',
    version='0.1',
    author='Everyone',
    author_email='',
    url='https://github.com/ingenieroariel/webandgis',
    description="Learn to build gis web systems",
    long_description=README,
    license='MIT, see LICENSE file.',
    install_requires=[
        'Django>=1.5',
        'django-leaflet',
        'pinax-theme-bootstrap',
        'python-safe>=1.1.2',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=['Topic :: Utilities',
                 'Natural Language :: English',
                 'Operating System :: OS Independent',
                 'Intended Audience :: Developers',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Development Status :: 2 - Pre-Alpha',
                 'Programming Language :: Python :: 2.7'],
)
