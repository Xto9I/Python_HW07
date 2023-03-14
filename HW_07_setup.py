from setuptools import setup

setup(
      name='clean_folder',
      version='1',
      description='script for cleaning folders',
      url='https://github.com/BogdanMotsak/python_core',
      author='Bogdan Motsak',
      author_email='bogdan.motsak@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']}
)



