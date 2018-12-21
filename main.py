from flask import Flask, jsonify, render_template, request
from api.test import tests
from api import project

app = Flask(__name__)

@app.route("/")
def index(name=None):
    return render_template('index.html')




app.register_blueprint(tests,url_prefix='/test')
app.register_blueprint(project.plist,url_prefix='/project')
app.register_blueprint(project.group,url_prefix='/project')
app.register_blueprint(project.item,url_prefix='/project')
app.register_blueprint(project.step,url_prefix='/project')
app.register_blueprint(project.report)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 80,debug = True)

