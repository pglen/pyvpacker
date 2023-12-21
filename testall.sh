#!/bin/bash

cd test_packer
echo -n "test0 "; python  testpacker.py   || exit 1
echo -n "test2 "; python  testpacker2.py  || exit 1
echo -n "test3 "; python  testpacker3.py  || exit 1
echo -n "test4 "; python  testpacker4.py  || exit 1
echo -n "test5 "; python  testpacker5.py  || exit 1
echo -n "test6 "; python  testpacker6.py  || exit 1
echo -n "test7 "; python  testpacker7.py  || exit 1
echo -n "test8 "; python  testpacker8.py  || exit 1
echo -n "test9 "; python  testpacker9.py  || exit 1

cd ..
