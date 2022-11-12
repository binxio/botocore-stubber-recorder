"""
generates test cases
"""
from os import path
from setuptools import find_packages, setup

dependencies = ['boto3', 'botostubs', 'jinja2', 'black', 'json-flatten']

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='botocore-stubber-recorder',
    version="0.4.3",
    url='https://github.com/binxio/botocore-stubber-recorder',
    license='BSD',
    author='Mark van Holsteijn',
    author_email='markvanholsteijn@binx.io',
    description='Records AWS boto calls and generates unit tests',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    package_data={'': ['templates/*']},
    packages=find_packages(where='src'),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=dependencies,
    setup_requires=[],
    tests_require=dependencies + ['pytest', 'botostubs', 'pytest-runner'],
    test_suite='tests',
    entry_points={
    },
    classifiers=[
        # As from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
