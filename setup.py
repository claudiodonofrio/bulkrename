from setuptools import setup

setup(
    name='bulkrename',
    version='0.1.0',
    py_modules=['bulkrename'],
    install_requires=[
        'Click','pillow'
    ],
    entry_points={
        'console_scripts': [
            'bulkrename = bulkrename:newname',
        ],
    },
)