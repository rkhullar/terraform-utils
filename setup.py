from setuptools import setup
from typing import Union
from pathlib import Path
import subprocess
import re


def read_file(path: Union[str, Path]) -> str:
    with Path(path).open('r') as f:
        return f.read().strip()


def infer_version() -> str:
    process = subprocess.run(['git', 'describe'], stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').strip()
    version = re.sub('^v', '', output)
    return version


setup(name='terraform-utils',
      version=infer_version(),
      url='https://github.com/rkhullar/terraform-utils',
      author='Rajan Khullar',
      author_email='rkhullar03@gmail.com',
      long_description=read_file('readme.md'),
      long_description_content_type='text/markdown',
      keywords='terraform terragrunt',
      license='MIT',
      packages=['terraform_utils'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose', 'parameterized'],
      entry_points={'console_scripts': ['tf-util=terraform_utils.command_line:main']}
      )
