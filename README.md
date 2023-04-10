# Data parsing package

## Installation:
   ```
   git clone https://github.com/enric-serra-sanz/fitfile
   python setup.py install
   ``` 

## Testing and building
Using tox for builds, flake for linting, and mypy for types.

You can simply run tox, to build for all available environments (this might fail if your system 
doesn't support a specific version of python).
```
pip install tox
tox
```

You can also build for a specific version:
```commandline
pip install tox
tox -e py38  # Will build python3.8 version 
```

To run the tests:
```commandline
python -m unittest
```

## Explanation:

This project gets data from some input files, applies rules to transform and validate the data
and then saves to an output in json format, it has been built with extension in mind.

It also assumes that you know the structure of your data beforehand, so you can provide what fields 
must undergo each transformation.

To execute the project:

```commandline
fitfile --json-file ./20230320_FITFILEPythonTest/PatientCohorts.json 
--csv-file ./20230320_FITFILEPythonTest/customer.csv 
--excel-file ./20230320_FITFILEPythonTest/ResearchList.xlsx --output-dir ./results
```

To print help 
```commandline
fitfile --help
```

## Note: 
I have only tested on python3.8
