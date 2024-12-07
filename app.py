from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Define the permanent part of the code with a placeholder for user code
PERMANENT_CODE = """
from graphviz import Digraph

g = Digraph('G', format='svg')

# USER CODE
# g.edge('Hello', 'World')

svg_string = g.pipe().decode('utf-8')
"""


# A function to execute Python code and capture the svg string
def execute_code(code):
    try:
        # Combine the permanent code with the user code
        full_code = PERMANENT_CODE.replace("# USER CODE", code)

        # Execute the combined code and capture the svg_string
        exec_globals = {}
        exec(full_code, exec_globals)

        # Extract the svg_string from the executed code's globals
        svg_string = exec_globals.get("svg_string", "")

        return svg_string
    except Exception as e:
        return str(e)


# Serve the index.html page
@app.route("/")
def index():
    return render_template("index.html", placeholder_code=PERMANENT_CODE)


# Handle the incoming code from the client and send back the output
@socketio.on("code_change")
def handle_code_change(code):
    output = execute_code(code)
    emit("output", {"output": output})


if __name__ == "__main__":
    socketio.run(app, debug=True)
