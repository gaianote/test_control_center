from flask import Blueprint,render_template, request,jsonify
from database import sqlite
import json
item = Blueprint('item',__name__)

@item.route("/item/")
def page():
    group_id = json.loads(request.args.get('group_id'))
    title = sqlite.fetchone('SELECT NAME FROM [GROUP] WHERE ID = ?',[group_id])[0]
    items = sqlite.fetchall('SELECT ID,NAME,INFO,CREATE_DATE,SORTORDER,IS_EXECUTE FROM ITEM WHERE GROUP_ID = ? AND IS_DELETED = 0 ORDER BY SORTORDER',[group_id])

    return render_template('project/item.html',title = title,items = items,group_id = group_id)

# projects manger
@item.route("/api/item/")
def item_api():
    a = request.args.get('name')
    b = request.args.get('info')
    return jsonify({'state':'success'})

@item.route("/api/item/delete")
def delete():
    item_id_list = json.loads(request.args.get('item_id_list'))
    print('item_id_list',item_id_list)
    for item_id in item_id_list:
        sqlite.execute('UPDATE ITEM set IS_DELETED = 1 WHERE ID = ?',[item_id])
    return jsonify({'state':'success'})
@item.route("/api/item/new")
def new():
    group_id = request.args.get('group_id')
    name = request.args.get('name')
    info = request.args.get('info')
    user = request.args.get('user')
    sqlite.execute('INSERT INTO [ITEM] (GROUP_ID,NAME,INFO,USER) VALUES (?,?,?,?)',[group_id,name,info,user])
    return jsonify({'state':'success'})


@item.route("/api/item/exorder")
def exorder():
    up_id,down_id = json.loads(request.args.get('item_id_list'))
    up_item_order = sqlite.fetchone('SELECT SORTORDER FROM [item] WHERE ID = ?',[up_id])[0]
    down_item_order = sqlite.fetchone('SELECT SORTORDER FROM [item] WHERE ID = ?',[down_id])[0]
    sqlite.execute("UPDATE [item] set SORTORDER = ? where id = ?",[down_item_order,up_id])
    sqlite.execute("UPDATE [item] set SORTORDER = ? where id = ?",[up_item_order,down_id])

    return jsonify({'state':'success'})
@item.route("/api/item/update")
def update():
    item_id = json.loads(request.args.get('item_id'))
    name = request.args.get('name')
    info = request.args.get('info')
    user = request.args.get('user')

    sqlite.execute("UPDATE [item] set NAME = ?,INFO = ?,USER = ? where id = ?",[name,info,user,item_id])
    return jsonify({'state':'success'})

@item.route("/api/item/state")
def state():
    item_id = request.args.get('item_id')
    is_execute = request.args.get('is_execute')
    sqlite.execute("UPDATE [item] set IS_EXECUTE = ? where id = ?",[is_execute,item_id])
    return jsonify({'state':'success'})

@item.route("/api/item/getprojectid")
def getprojectid():
    group_id = request.args.get('group_id')
    project_id = sqlite.fetchone('SELECT PROJECT_ID FROM [GROUP] WHERE ID = ?',[group_id])[0]
    return jsonify({'state':'success','project_id':project_id})