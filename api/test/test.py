

from flask import Blueprint,render_template, request,jsonify
tests = Blueprint('admin',__name__)
# projects manger
@tests.route("/test/")
def test():
    return render_template('test.html')

@tests.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

