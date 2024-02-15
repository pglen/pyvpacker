import setuptools

descx = '''

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
    name="pypacker",
    version="1.0",
    author="Peter Glen",
    author_email="peterglen99@gmail.com",
    description="Pack python data onto a string.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pglen/pydpacker",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(include=includex),

    #scripts = ['pypacker.py'],
    py_modules = ["pypacker", "tests" ],
    #package_dir = {'': 'tests', 'tests':'test_packer'},

    python_requires='>=3',

    #entry_points={
    #    'console_scripts': [ "pydbase=pydbase:mainfunc", ],
    #}
)

# EOF
