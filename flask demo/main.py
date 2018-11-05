from flask import *
app = Flask(__name__, static_url_path='')
app.debug = True

@app.route("/")
def render_static():
    return "hello world"

@app.route("/help")
def help():
    return "there is no help"

@app.route("/hello/<name>")
def person(name):
    return render_template("index.html", name=name)

@app.route("/form", methods = ['POST', 'GET'])
def form():
    if request.method == 'POST':
        result = request.form 
        return render_template("form.html", result=result, send=True)
    else:
        return render_template("form.html", send=False)

# @app.route("/result", methods = ['POST', 'GET'])
# def process_form():
#     if request.method == 'POST':
#         result = request.form 
#         return render_template("form.html", result=result)

if __name__ == '__main__':
    app.run()
