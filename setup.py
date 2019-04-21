from setuptools import setup
from typing import Union
from pathlib import Path


def read_file(path: Union[str, Path]) -> str:
    with Path(path).open('r') as f:
        return f.read().strip()


setup(name='terraform-utils',
      version=read_file('version.txt'),
      url='https://github.com/rkhullar/terraform-utils',
      author='Rajan Khullar',
      author_email='rkhullar@nyit.edu',
      long_description=read_file('readme.md'),
      keywords='terraform terragrunt',
      license='MIT',
      packages=['terraform_utils'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],
      entry_points={'console_scripts': ['tf-util=terraform_utils.command_line:main']}
      )
