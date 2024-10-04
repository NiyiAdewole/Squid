from setuptools import setup, find_packages

setup(
    name='schema_generator',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'Flask',
        'pandas',
        'openpyxl',
    ],
    entry_points='''
        [console_scripts]
        schema_generator=app.cli:main
    ''',
)
