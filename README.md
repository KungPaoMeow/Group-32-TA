## How to run the starter project

1. Make sure you are in the root directory of the project.
2. In the root directory, create a virtual environment by running the following command:

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
1. Make sure you are in the root directory of the project and the virtual environment is activated.
2. To run a <testfile> in the tests/ directory, run:
    ```bash
    python -m unittest tests/<testfile>
    ```