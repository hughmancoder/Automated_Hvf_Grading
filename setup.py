from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

# TODO: Add Liscense
# with open('LICENSE') as f:
#     license = f.read()

setup(
    name='automated_hvf_grading',
    version='0.1.0',
    description='Automates HVF Grading',
    long_description=readme,
    author='Hugh, Sonel',
    author_email='hugh.signoriello@gmail.com',
    url='https://github.com/hughmancoder/automated-hvf-grading',
    # license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)