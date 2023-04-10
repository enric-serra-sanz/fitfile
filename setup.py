from setuptools import setup, find_packages

test_requirements = ['pytest'],

setup(
    name='fitfile',
    version='0.0.1',
    packages=find_packages('src'),
    install_requires=[
        'types-python-dateutil',
        'mock',
        'faker',
        'data-science-types',
        'pandas~=2.0.0',
        'openpyxl',
        "coverage",
    ],
    tests_require=test_requirements,
    license='',
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Dev/Ops',
        'Topic :: Software Development :: Test',

        # Pick your license as you wish (should match "license" above)
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='data tranformation',
    author='Enric Serra Sanz',
    author_email='enricserrasanz@gmail.com',
    description='A very basic ETL toolsrc'
)