# Environment Setup for Assignments
All assignments must be run using **Python ≥ 3.12.3** inside a **virtual environment (venv)**.  
Running inside a venv ensures that package versions are isolated, reproducible, and do not interfere with system Python.

You can check your Python version with:
```bash
python3 --version
```


## Creating a Virtual Environment

From the project root, create and activate a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

**On macOS / Linux**
```bash
source venv/bin/activate
```

**On Windows (PowerShell)**
```powershell
venv\Scripts\Activate.ps1
```

Once activated, your shell prompt should show `(venv)`.


## Installing Required Packages

Install the required packages inside the virtual environment:

```bash
pip3 install coverage aiohttp requests
```

Or install using the given requirement file
```bash
pip3 install -r requirement.txt
```


## Running Coverage

Within the virtual environment, the `coverage` package can be executed in two equivalent ways:

### 1. Using the installed binary
Among installation of coverage package, a binary tool is also installed and added to your PATH. Hence you can run it with:
```bash
coverage run -m pytest
coverage report
```

### 2. Using the Python module
This method is more robust and always uses the correct Python interpreter:
```bash
python -m coverage run -m pytest
python -m coverage report
```

Both methods invoke the same `coverage` package; the second form avoids issues with incorrect `PATH` or mismatched Python installations.
