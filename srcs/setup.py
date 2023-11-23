from setuptools import find_packages, setup

setup(
    name='tcommons',
    version='1.0.0',
    packages=find_packages(include=['tcommons', 'tcommons.*']),
    include_package_data=True,
    install_requires=[
        'Django>=4.2.7',
    ],
    # Other metadata
    author='',
    author_email='',
    description='A common package for the Transcendence project',
    # long_description=open('README.md').read(),
    # long_description_content_type='text/markdown',
    url='https://github.com/diegosanchezstrange/transcendence',
    # More metadata
)

