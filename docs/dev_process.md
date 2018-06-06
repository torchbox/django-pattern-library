# Overview

This document contains information for project developers.

## How to build the package

To build the package you need to Python 3 and Nodejs 8.

Install FE dependencies and build static:

```
npm install
npm run build
```

Build the python package:

```
virtualenv -p python3.6 venv
source venv/bin/activate
python ./setup.py bdist_wheel
```
