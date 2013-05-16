import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='webandgis',
    version='0.1',
    author='Everyone',
    author_email='',
    url='https://github.com/ingenieroariel/webandgis',
    description="Learn to build gis web systems",
    long_description=open(os.path.join(here, 'README.md')).read() + '\n\n' +
                     open(os.path.join(here, 'CHANGES')).read(),
    license='MIT, see LICENSE file.',
    install_requires=[
                      'Django',
                      'django-leaflet',
                      'django-bootstrap',
                   ],
    packages=find_packages(),
    include_package_data = True,
    zip_safe = False,
    classifiers = ['Topic :: Utilities',
                    'Natural Language :: English',
                    'Operating System :: OS Independent',
                    'Intended Audience :: Developers',
                    'Environment :: Web Environment',
                    'Framework :: Django',
                    'Development Status :: 2 - Pre-Alpha',
                    'Programming Language :: Python :: 2.7'],
)
