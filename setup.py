from ast import literal_eval
from distutils.core import setup


def get_version(source='petlx/__init__.py'):
    with open(source) as f:
        for line in f:
            if line.startswith('__version__'):
                return literal_eval(line.split('=')[-1].lstrip())
    raise ValueError("__version__ not found")


setup(
    name='petlx',
    version=get_version(),
    author='Alistair Miles',
    author_email='alimanfoo@googlemail.com',
    package_dir={'': '.'},
    packages=['petlx', 'petlx.test'],
    url='https://github.com/alimanfoo/petlx',
    license='MIT License',
    description='Optional extensions for the petl package.',
    long_description=open('README.txt').read(),
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.4',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ],
    install_requires=['petl>=1.0']
)
