from flask import Blueprint,render_template, request,jsonify
from database import sqlite
import json
from lib import get_funcname,get_file_list
step = Blueprint('step',__name__)


# 根据项目id返回测试用例
@step.route("/step/")
def page():
    item_id = json.loads(request.args.get('item_id'))
    title = sqlite.fetchone('SELECT NAME FROM ITEM WHERE ID = ?',[item_id])[0]
    items = sqlite.fetchall('SELECT ID,DESCRIPTION,METHOD,VALUE,IS_EXECUTE FROM STEP WHERE item_id = ? AND IS_DELETED = 0 ORDER BY SORTORDER',[item_id])


    return render_template('project/step.html',title = title,items = items,item_id = item_id)

@step.route("/api/step/delete")
def delete():
    step_id_list = json.loads(request.args.get('step_id_list'))
    for step_id in step_id_list:
        sqlite.execute('UPDATE STEP set IS_DELETED = 1 WHERE ID = ?',[step_id])
    return jsonify({'state':'success'})
@step.route("/api/step/new")
def new():
    item_id = request.args.get('item_id')
    description = request.args.get('description')
    method = request.args.get('method')
    value = request.args.get('value')
    print(item_id)
    sqlite.execute('INSERT INTO STEP (ITEM_ID,DESCRIPTION,METHOD,VALUE) VALUES (?,?,?,?)',[item_id,description,method,value])

    return jsonify({'state':'success'})


@step.route("/api/step/exorder")
def exorder():
    up_id,down_id = json.loads(request.args.get('step_id_list'))
    print(up_id,down_id)
    up_step_order = sqlite.fetchone('SELECT SORTORDER FROM [step] WHERE ID = ?',[up_id])[0]
    down_step_order = sqlite.fetchone('SELECT SORTORDER FROM [step] WHERE ID = ?',[down_id])[0]
    sqlite.execute("UPDATE [step] set SORTORDER = ? where id = ?",[down_step_order,up_id])
    sqlite.execute("UPDATE [step] set SORTORDER = ? where id = ?",[up_step_order,down_id])

    return jsonify({'state':'success'})
@step.route("/api/step/update")
def update():
    step_id = json.loads(request.args.get('step_id'))
    description = request.args.get('description')
    method = request.args.get('method')
    value = request.args.get('value')

    sqlite.execute("UPDATE [step] set DESCRIPTION = ?,METHOD = ?,VALUE = ? where id = ?",[description,method,value,step_id])
    return jsonify({'state':'success'})

@step.route("/api/step/state")
def state():
    step_id = request.args.get('step_id')
    is_execute = request.args.get('is_execute')
    sqlite.execute("UPDATE [step] set IS_EXECUTE = ? where id = ?",[is_execute,step_id])
    return jsonify({'state':'success'})

@step.route("/api/step/getfuncdata")
def getfuncdata():
    file_list = get_file_list('/mnt/c/Users/gaianote/Desktop/center_test/zeus','.py')

    func_list,func_dict = get_funcname(file_list)
    return jsonify({'state':'success','project_function_list':func_list,'project_function_dict':func_dict})


@step.route("/api/step/getgroupid")
def getgroupid():
    item_id = request.args.get('item_id')
    group_id = sqlite.fetchone('SELECT GROUP_ID FROM ITEM WHERE ID = ?',[item_id])[0]
    return jsonify({'state':'success','group_id':group_id})







