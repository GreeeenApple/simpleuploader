# -*- coding: utf-8 -*-

from flask import *
import werkzeug
import os
import subprocess
import shlex

class LimitedRequest(Request):
    max_form_memory_size = 1024 * 1024 * 30

app = Flask(__name__)
app.request_class = LimitedRequest

@app.route("/", methods=["GET"])
def index():
    files = os.listdir("./files/")
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    f.save("./files/" + werkzeug.secure_filename(f.filename))
    return redirect("/")

@app.route("/download", methods=["GET"])
def download():
    filename = request.args.get("filename")
    
    if filename in os.listdir("./files/"):
        filename = werkzeug.secure_filename(filename)
        
        response = make_response()
        
        try:
            response.data = open("./files/" + filename, "rb").read()
        except:
            return "ERROR!"
        
        response.headers["Content-type"] = "application/octet-stream"
        response.headers["Content-Disposition"] = u"attachment; filename=" + filename

        return response
    else:
        return "Error Not Found File!"

@app.route("/delete", methods=["GET"])
def delete():
    filename = request.args.get("filename")
    
    if filename in os.listdir("./files/"):
        filename = werkzeug.secure_filename(filename)
        subprocess.check_output(shlex.split("rm ./files/" + filename))

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
