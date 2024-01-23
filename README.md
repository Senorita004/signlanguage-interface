# Running the Python Flask Server

## 1. Navigate to Your Project Directory
Open your command line or terminal and navigate to the directory where your Python script is located.

```bash
cd path/to/your/project
```

## 2. Activate the Virtual Environment
If you're using a virtual environment, activate it.

On Windows:
bash
```bash
.\venv\Scripts\activate
```

On MacOS/Linux:
```bash
source venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Run the Flask Application
Set the FLASK_APP environment variable and run the Flask app.

On Windows:
```bash
set FLASK_APP=app.py
flask run --port=8000
```

On MacOS/Linux:
```bash
export FLASK_APP=app.py
flask run --port=8000
```

```bash
python app.py
```
4. Accessing the Server
The server will typically be accessible at http://127.0.0.1:8000 or http://localhost:8000.

5. Using the API
Send requests to the server's endpoint, like http://127.0.0.1:8000/predict, using a tool like curl, Postman, or an HTTP client in a programming language.

6. Stop the Server
To stop the server, press Ctrl + C in the terminal.