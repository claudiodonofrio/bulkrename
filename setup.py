from setuptools import setup

setup(
    name='bulkrename',
    version='0.1.0',
	author="Claudio D'Onofrio",
    author_email='claudio.donofrio@gmail.com', 
    py_modules=['bulkrename'],
    install_requires=[
        'Click','pillow', 'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'bulkrename = bulkrename:newname',
        ],
    },
)