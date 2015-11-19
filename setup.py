from setuptools import setup

setup(
    name='spinup',
    packages=['spinup'],
    version='0.1',
    description='Spinup nginx virtual servers and hosts file entries.',
    author='Phil Eaton',
    author_email='me@eatonphil.com',
    url='https://github.com/eatonphil/spinup',
    download_url='https://github.com/eatonphil/spinup/tarball/0.1',
    keywords=['nginx', 'virtual', 'hosts'],
    entry_points={
        'console_scripts': [
            'spinup = spinup.spinup:main'
        ]
    }
)
