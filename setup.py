import setuptools

descx = '''

  Pack python array into a string, and matching unpack
  routines as well. Python 3.

'''

classx = [
          'Development Status :: Mature',
          'Environment :: GUI',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Databases',
        ]

includex = ["*", ]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyvpacker",
    version="1.1",
    author="Peter Glen",
    author_email="peterglen99@gmail.com",
    description="Pack python data onto a string.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pglen/pyvpacker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(include=includex),

    scripts = ['demopacker.py'],
    py_modules = ['pyvpacker'],
    #package_dir = {'': '.', }, #'tests':'test_packer'},

    python_requires='>=3',

    entry_points={
        'console_scripts': [ "demopacker=demopacker:mainfunc", ],
    }
)

# EOF
