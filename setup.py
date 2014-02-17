from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='capitalist-nomad',
    author='Thomas Levine',
    author_email='_@thomaslevine.com',
    description='Find situations where people are going away for a few weeks and renting out their houses',
    long_description=long_description,
    url='https://github.com/tlevine/undervalued-sublets.git',
    classifiers=[
    ],
    packages=['craigsgenerator'],

    install_requires = ['craigsgenerator'],

    version='0.0.1',
    license='AGPL'
)
