"""
MVw
---
Minimal Viable Wiki
"""
from setuptools import setup, find_packages

setup(
    name='MVW',
    version='0.1pre',
    url='http://simplectic.com/mvw/',
    license='MIT',
    author='Kevin Beaty',
    author_email='kevin@simplectic.com',
    description='A minimal personal wiki engine',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Jinja2',
        'Markdown',
        'Pygments',
    ],
    entry_points={
      'console_scripts': [
          'mvw = mvw.main:run'
      ]
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
)
