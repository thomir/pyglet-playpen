from setuptools import setup, find_packages


setup(
    name="pg",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pyglet',
    ],
    entry_points={
        'console_scripts': [
            'pg = pg.cli:main',
        ],
    },
    test_suite='pg.tests',
    test_requires=[
        'hypothesis',
    ],
    include_package_data=True,
)
