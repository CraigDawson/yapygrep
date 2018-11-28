from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="yapgrep",
    version="0.6",
    author="Whiteboard Programming Group",
    author_email="craigdawson@gmail.com",
    description="Yet another python GREP",
    long_description=long_description,
    url="https://github.com/CraigDawson/yapygrep",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '': ['data/types.json'],
        },
    scripts=['bin/yapgrep'],
)
