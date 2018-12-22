from flask import Blueprint,render_template, request,jsonify
from database import sqlite
from lib import Generator
import json
import os
from config import config
import subprocess
report = Blueprint('report',__name__)

@report.route("/report/")
def report_list():
    project_id = json.loads(request.args.get('project_id'))

    title = sqlite.fetchone('SELECT NAME FROM PROJECT WHERE ID = ?',[project_id])[0]
    if sqlite.fetchone('SELECT STATE FROM PROJECT WHERE ID = ?',[project_id])[0] == 'COMPLETE':
        sqlite.execute('UPDATE PROJECT SET STATE = "FREE" WHERE ID = ?',[project_id])
    groups = sqlite.fetchall('SELECT ID,CREATE_DATE,END_DATE,STATE FROM REPORT WHERE PROJECT_ID = ? ORDER BY ID DESC',[project_id])
    # os.path.join(config.reportpath,'{:0>8d}.html'.format(report_id))
    return render_template('project/report.html',title = title,project_id = project_id,projects_list = groups)
@report.route("/api/report/detail")
def report_detail():
    report_id = json.loads(request.args.get('report_id'))
    return render_template('report/{:0>8d}.html'.format(int(report_id)))

@report.route("/api/report/delete")
def delete_project():
    report_id_list = json.loads(request.args.get('report_id_list'))
    for report_id in report_id_list:
        sqlite.execute('DELETE FROM REPORT WHERE ID = ?',[report_id])
        try:
            os.remove(os.path.join(config.reportpath,'{:0>8d}.html'.format(int(report_id))))
        except Exception as e:
            print(e)
    return jsonify({'state':'success'})