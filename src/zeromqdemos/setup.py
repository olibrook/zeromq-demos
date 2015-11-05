from setuptools import setup, find_packages

setup(
    name="zeromqdemos",
    version="0.0.1",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "pyzmq==15.0.0",
        "docopt==0.6.2",
    ],
    entry_points={
        'console_scripts': [
            'producer=zeromqdemos.producer:main',
            'consumer=zeromqdemos.consumer:main',
            'collector=zeromqdemos.collector:main',
            'zeromqdemos-main=zeromqdemos.main:main',
        ]
    },
)
