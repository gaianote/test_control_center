from flask import Blueprint,render_template, request,jsonify
new = Blueprint('new',__name__)
# projects manger
@new.route("/new/")
def newpage():
    return render_template('project/new.html')


