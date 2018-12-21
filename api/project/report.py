from flask import Blueprint,render_template, request,jsonify
from database import sqlite
from lib import Generator
import json
import os
import subprocess
report = Blueprint('reportreport',__name__)

@report.route("/report/")
def page():
    return render_template('report/20181221_164431.html')

@report.route("/report/list")
def report_list():
    groups = sqlite.fetchall('SELECT ID,NAME,INFO,CREATE_DATE,SORTORDER,IS_EXECUTE FROM PROJECT WHERE IS_DELETED = 0 ORDER BY SORTORDER')
    return render_template('project/report.html',projects_list = groups)
