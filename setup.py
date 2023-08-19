from setuptools import setup
import bulkrename


setup(
    name='bulkrename',
    version=bulkrename.__version__,
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