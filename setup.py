from setuptools import setup

setup(name='Playlistr',
    version='1.0',
    description='Generate Youtube playlists from text',
    author='Guido Arnau',
    author_email='guido.arnau@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Flask>=0.10.1', 'google-api-python-client>=1.4.2'],
    )
