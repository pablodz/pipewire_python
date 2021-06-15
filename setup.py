from setuptools import setup

setup(
    name='pipewire_python',
    version='0.0.1',
    description='Pipewire Python Manager (Record, play, create virtual devices)',
    author='Pablo Diaz & Anna Absi',
    url='https://github.com/pablodz/pipewire_python',
    license='MIT',
    packages=['pipewire_python'], 
    package_data={'pipewire_python': ['*.py']},
    install_requires=['numpy'],
    python_requires='>=3.7',    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
)