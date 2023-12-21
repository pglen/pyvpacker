#!/bin/bash

cd tests
pytest
# For this python2 and python 2 pytest needs to be installed
python2 -m pytest
cd ..

