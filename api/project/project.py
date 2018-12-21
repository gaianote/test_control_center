from flask import Blueprint,render_template, request,jsonify
from database import sqlite
from lib import Generator
import json
import os
import subprocess
plist = Blueprint('plist',__name__)

@plist.route("/plist/")
def page():
    groups = sqlite.fetchall('SELECT ID,NAME,INFO,CREATE_DATE,SORTORDER,IS_EXECUTE FROM PROJECT WHERE IS_DELETED = 0 ORDER BY SORTORDER')
    return render_template('project/plist.html',projects_list = groups)


@plist.route("/api/plist/delete")
def delete_project():
    project_id_list = json.loads(request.args.get('project_id_list'))
    for project_id in project_id_list:
        sqlite.execute('UPDATE PROJECT set IS_DELETED = 1 WHERE ID = ?',[project_id])
    return jsonify({'state':'success'})

@plist.route("/new/")
def new_page():
    return render_template('project/new.html')

@plist.route("/api/new/")
def new_api():
    name = request.args.get('name')
    info = request.args.get('info')
    user = 'user'
    project_id = sqlite.execute('INSERT INTO PROJECT (NAME,INFO,USER) VALUES (?,?,?)',[name,info,user])
    return jsonify({'state':'success','project_id':project_id})

@plist.route("/api/plist/exorder")
def exorder():
    up_id,down_id = json.loads(request.args.get('project_id_list'))

    up_project_order = sqlite.fetchone('SELECT SORTORDER FROM project WHERE ID = ?',[up_id])[0]
    down_project_order = sqlite.fetchone('SELECT SORTORDER FROM project WHERE ID = ?',[down_id])[0]
    sqlite.execute("UPDATE project set SORTORDER = ? where id = ?",[down_project_order,up_id])
    sqlite.execute("UPDATE project set SORTORDER = ? where id = ?",[up_project_order,down_id])

    return jsonify({'state':'success'})
@plist.route("/api/plist/state")
def state():
    project_id = request.args.get('project_id')
    is_execute = request.args.get('is_execute')
    sqlite.execute("UPDATE PROJECT set IS_EXECUTE = ? where id = ?",[is_execute,project_id])
    return jsonify({'state':'success'})

@plist.route("/api/plist/update")
def update():
    project_id = json.loads(request.args.get('project_id'))
    name = request.args.get('name')
    info = request.args.get('info')
    user = request.args.get('user')
    sqlite.execute("UPDATE PROJECT set NAME = ?,INFO = ?,USER = ? where id = ?",[name,info,user,project_id])
    return jsonify({'state':'success'})

@plist.route("/api/plist/exeute")
def exeute():
    project_path = '/mnt/c/Users/00807/Desktop/resilio/toyou/code/核心测试用例/center_test/'
    test_dir_path = 'test'
    entry_file = 'main.py'

    generator = Generator(os.path.join(project_path,test_dir_path))
    project_id = json.loads(request.args.get('project_id'))
    groups = sqlite.fetchall('SELECT NAME,ID FROM [GROUP] WHERE PROJECT_ID = ? AND IS_DELETED = 0 AND IS_EXECUTE = "checked"',[project_id])
    for group in groups:
        order = sqlite.fetchone('SELECT SORTORDER FROM [GROUP] WHERE ID = ? AND IS_DELETED = 0 AND IS_EXECUTE = "checked"',[group[1]])
        generator.gengroup(group[0],order[0])
        items = sqlite.fetchall('SELECT NAME,ID FROM ITEM WHERE GROUP_ID = ? AND IS_DELETED = 0 AND IS_EXECUTE = "checked"',[group[1]])
        print(items)
        for item in items:
            generator.genitem(item[0])
            steps = sqlite.fetchall('SELECT METHOD,VALUE FROM STEP WHERE ITEM_ID = ? AND IS_DELETED = 0 AND IS_EXECUTE = "checked"',[item[1]])
            for step in steps:
                generator.genstep(step[0],step[1])
    subprocess.Popen(['python3',os.path.join(project_path,entry_file)])
    return jsonify({'state':'success'})