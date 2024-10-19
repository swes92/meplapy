from setuptools import setup, find_packages

setup(
    name='meplapy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pdfplumber',
        'nltk',
        'argparse',
        'geopy',
        'folium',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'meplapy = meplapy.cli:main',  # Command-line tool entry point
        ],
    },
    description='A tool for geolocating and mapping places mentioned in documents.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/swes92/meplapy',
    author='Your Name',
    author_email='your.email@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
