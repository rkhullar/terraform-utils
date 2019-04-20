from setuptools import setup


def version():
    with open('version.txt', 'r') as f:
        return f.read().strip()


def readme():
    with open('readme.md', 'r') as f:
        return f.read()


setup(name='terraform-utils',
      version=version(),
      url='https://github.com/rkhullar/terraform-utils',
      author='Rajan Khullar',
      author_email='rkhullar@nyit.edu',
      long_description=readme(),
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
