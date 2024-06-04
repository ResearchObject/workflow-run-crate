# SPARQL queries for the Competency Questions

This directory contains SPARQL queries corresponding to the [Competency Questions](https://www.researchobject.org/workflow-run-crate/requirements) (CQs). Each query is contained in a Python script named after the CQ itself, e.g. `cq6.py`, which contains:

* A docstring with documentation on the CQ
* The SPARQL query in a string variable named `QUERY`
* The code needed to run the query and display the results on the terminal

To run the script we suggest creating a virtual environment and install the prerequisites:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

After this, you can simply run a query by running the corresponding script:

```console
$ python cq6.py 
2023-02-21T12:44:53.363530, 2023-02-21T12:45:11.260305
```
