from setuptools import setup, find_packages
setup(name='wg',
      version='0.1',
      author='Nick Clarke',
      author_email='nickolasclarke@gmail.com',
      description = 'A Flask-driven API for WG',
      url='https://github.com/nickolasclarke/wghw',
      packages=find_packages(),
      classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
      ],
      python_requires='>=3.5',
      )