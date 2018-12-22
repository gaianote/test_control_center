from flask import Blueprint,render_template, request,jsonify
import database
from database import sqlite
import json
import time
group = Blueprint('group',__name__)

@group.route("/group/")
def page():
    project_id = json.loads(request.args.get('project_id'))
    title = sqlite.fetchone('SELECT NAME FROM PROJECT WHERE ID = ?',[project_id])[0]
    groups = sqlite.fetchall('SELECT ID,NAME,INFO,CREATE_DATE,SORTORDER,IS_EXECUTE FROM [GROUP] WHERE PROJECT_ID = ? AND IS_DELETED = 0 ORDER BY SORTORDER',[project_id])
    return render_template('project/group.html',title = title,items = groups,project_id = project_id)


@group.route("/api/group/delete")
def delete():
    group_id_list = json.loads(request.args.get('group_id_list'))

    for group_id in group_id_list:
        sqlite.execute('UPDATE [group] set IS_DELETED = 1 WHERE ID = ?',[group_id])
    return jsonify({'state':'success'})

@group.route("/api/group/new")
def new():
    project_id = request.args.get('project_id')
    name = request.args.get('name')
    info = request.args.get('info')
    user = request.args.get('user')
    sqlite.execute('INSERT INTO [GROUP] (PROJECT_ID,NAME,INFO,USER) VALUES (?,?,?,?)',[project_id,name,info,user])
    return jsonify({'state':'success'})

@group.route("/api/group/exorder")
def exorder():
    up_id,down_id = json.loads(request.args.get('group_id_list'))

    up_group_order = sqlite.fetchone('SELECT SORTORDER FROM [GROUP] WHERE ID = ?',[up_id])[0]
    down_group_order = sqlite.fetchone('SELECT SORTORDER FROM [GROUP] WHERE ID = ?',[down_id])[0]
    sqlite.execute("UPDATE [group] set SORTORDER = ? where id = ?",[down_group_order,up_id])
    sqlite.execute("UPDATE [group] set SORTORDER = ? where id = ?",[up_group_order,down_id])

    return jsonify({'state':'success'})
@group.route("/api/group/update")
def update():
    group_id = json.loads(request.args.get('group_id'))
    name = request.args.get('name')
    info = request.args.get('info')
    user = request.args.get('user')
    print(group_id,name,info,user)
    sqlite.execute("UPDATE [group] set NAME = ?,INFO = ?,USER = ? where id = ?",[name,info,user,group_id])
    return jsonify({'state':'success'})

@group.route("/api/group/state")
def state():
    group_id = request.args.get('group_id')
    is_execute = request.args.get('is_execute')
    sqlite.execute("UPDATE [group] set IS_EXECUTE = ? where id = ?",[is_execute,group_id])
    return jsonify({'state':'success'})