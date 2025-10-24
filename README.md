# Pharmacy Management System
Course project for [CISC 327 - Software Quality Assurance](https://www.cs.queensu.ca/undergraduate/courses/CISC-327) at Queen's University with a focus on testing methods.

## How to run the project

1. Make sure you are in the `flask_app` directory.
2. Create a virtual environment by running the following command:

    ```bash
    python3 -m venv venv
    ```
    Here the second `venv` is the name of the virtual environment. You can use any name you want.

3. Activate the virtual environment by running the following command:

    Bash:
    ```bash
    source venv/Scripts/activate 
    ```

    Windows CMD:
    ```bash
    venv\Scripts\activate
    ```

    PowerShell:
    ```bash
    venv\Scripts\Activate.ps1
    ```

4. Install the required packages by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

5. Run the following command to start the server:

    ```bash
    python app.py
    ```

    Flask default port is 5000, if you are getting "attempt was made to access a socket in a way forbidden..." error try:

    Bash:
    ```bash
    FLASK_APP=app.py flask run --port=5001
    ```

    Windows CMD:
    ```bash
    set FLASK_APP=app.py && flask run --port=5001
    ```

    To run in development env add: 
    ```bash 
    FLASK_ENV=development 
    ```

## How to run test files
# Unit tests and integration tests
1. Make sure you are in the `flask_app` directory and the virtual environment is activated.
2. To run a `<testfile>` in the `flask_app/tests/` directory, run:
    ```bash
    python -m unittest tests/<testfile>
    ```
# End to end (selenium) tests
1. Make sure you have Google Chrome
2. Make sure the app is currently running (follow instructions to run the project if it is not)
3. Run the `flask_app/tests/e2e_tests.py` file

## How to run code coverage
1. Make sure you are in the `flask_app` directory and the virtual environment is activated.
2. To run a coverage report on a `<testfile>` in the `flask_app/tests/` directory, run:
    ```bash
    coverage run -m unittest tests/<testfile>
    ```
3. To view the coverage report, run:
    ```bash
    coverage report
    ```
4. To view the coverage report in detail, run:
    ```bash
    coverage html
    ```
    This creates a `htmlcov` folder, open it and locate `index.html`, and open it in your browser to view the detailed report.