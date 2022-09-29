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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
)