from distutils.core import setup

setup(
    name='petlx',
    version='0.1',
    author='Alistair Miles',
    author_email='alimanfoo@googlemail.com',
    package_dir={'': 'src'},
    packages=['petlx'],
    url='https://github.com/alimanfoo/petlx',
    license='MIT License',
    description='Optional extensions for the petl package.',
    long_description=open('README.txt').read(),
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ],
    requires=['petl (>=0.3)']  
)
