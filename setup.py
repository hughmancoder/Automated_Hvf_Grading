from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sample',
    version='0.1.0',
    description='automated-hvf-grading',
    long_description=readme,
    author='Hugh, Sonel',
    author_email='hugh.signoriello@gmail.com',
    url='https://github.com/hughmancoder/automated-hvf-grading',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)