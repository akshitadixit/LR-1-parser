from tabler import LR1
from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

def main_func(gram, string):
    f= open(gram,"r")
    lines = []
    counter = 0
    nt = []
    t = []
    prod = {}
    for line in f:
        line = line.split()
        if(counter == 0):
            nt += line
        elif(counter == 1):
            t += line
        else:
            index = line.pop(0)
            if(index not in prod.keys()):
                prod[index] = []
            prod[index].append(tuple())
            for i in line:
                prod[index][len(prod[index])-1] += tuple(i)
        counter += 1
    lr = LR1(nt, t, prod)
    table = lr.construct()
    stack, res = lr.parser(table, string)
    return [table, stack, res, nt, t]


@app.route("/", methods=['GET', 'POST'])
def start():
    return render_template("index.html")

@app.route("/table", methods=['GET', 'POST'])
def tabler():
    table = []
    return render_template("index.html", table)

@app.route("/parse", methods=['GET', 'POST'])
def parser():
    result = 0
    return render_template("index.html", result)

@app.route("/input", methods=['POST'])
def take_input():
    f = request.files['grammar']
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
    f.save(file_path)

    string =  str(request.form.get("string", False))
    print(file_path)
    print(string)
    data = main_func(file_path, string)
    print(len(data), ' data= ', data)
    data = [data[0], data[1], data[2], data[3]+data[4]+['$']]
    return render_template("table.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)