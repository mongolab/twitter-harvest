from distutils.core import setup

setup(
        name='harvest',
        version='1.0',
        description='Twitter User Timeline Harvest',
        author='Mongolab',
        author_email='support@mongolab.com',
        package_dir={'':'lib'},
        packages=['pymongo', 'oauth2', 'bson', 'httplib2']
    )
