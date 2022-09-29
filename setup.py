from setuptools import setup

setup(
    name='qtmtracker',
    version='0.0.1',    
    description='Easily gather 3D tracking data from Qualisys Track Manager (QTM).',
    url='https://github.com/zeyus/qtmtracker',
    author='zeyus',
    author_email='python@zeyus.com',
    license='MIT',
    packages=['qtmtracker'],
    install_requires=['qtm'],

    classifiers=[
        'Intended Audience :: Science/Research',,
        'Programming Language :: Python :: 3',
    ],
)