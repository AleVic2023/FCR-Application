from flask import Flask

app: Flask = Flask('_name_')


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if '_name_' == "_main_":
    app.run()



import os

fn=r"C:\Users\ca-rodriguez-jaime\FCR-Application>python FCR-Application/Preuve flask.py"
newfn=fn.replace(os.sep,'/')