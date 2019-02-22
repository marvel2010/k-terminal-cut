from setuptools import setup
from setuptools import find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def license():
    with open('LICENSE') as f:
        return f.read()


setup(name='ktcut',
      version='0.1dev',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      description='k-Terminal Cut Solver',
      keywords='',
      url='https://github.com/marvel2010/k-terminal-cut',
      author='Mark Velednitsky',
      author_email='marvel@berkeley.edu',
      license=license(),
      long_description=readme(),
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['numpy', 'networkx'],
      setup_requires=['pytest-runner', ],
      tests_require=['pytest', ],
      zip_safe=False
      )

