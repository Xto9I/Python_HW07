from setuptools import setup

setup(
      name='clean_folder',
      version='1',
      description='Performs cleaning and sorting in folders',
      url='https://github.com/KatePomazunova/GoIT_Homework/blob/main/DZ_6_mod.py',
      author='Kateryna Pomazunova',
      author_email='kateryna.pomazunova@gmail.com',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:start_sort']}
)