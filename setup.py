from setuptools import setup

setup(
    name='trafficstars',
    version='1.0.1',
    description='TrafficStars API Client',
    url='https://github.com/Romamo/python-trafficstars',

    author='Romamo',
    author_email='romamo@yandex.ru',
    license='MIT',

    packages=['trafficstars'],

    install_requires=[],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    zip_safe=False,
)