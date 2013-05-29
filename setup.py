from distutils.core import setup

setup(
        name='Harvest',
        version='1.0',
        description='Twitter User Timeline Harvest',
        author='The MongoLab Team',
        author_email='team@mongolab.com',
        url='https://github.com/c2chang/twitter-harvest',
        install_requires=['pymongo','oauth2','bson','httplib2']
    )

#package_dir={'':'lib'},
#packages=['pymongo', 'oauth2', 'bson', 'httplib2']
