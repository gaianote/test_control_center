from flask import Blueprint,render_template, request,jsonify
import database
edit = Blueprint('edit',__name__)

# 根据项目id返回测试用例
@edit.route("/edit/")
def edit_page():
    project_id = request.args.get('project_id')
    title,items = database.project.get_item_list(project_id)
    return render_template('project/edit.html',title = title,items = items,project_id = project_id)

# projects manger
@edit.route("/api/edit/")
def lists_api():
    project_id = request.args.get('project_id')
    print(project_id)
    return jsonify({'state':'success'})

# 创建一个测试用例
@edit.route("/api/new_item")
def new():
    project_id = request.args.get('project_id')
    name = request.args.get('name')
    info = request.args.get('info')
    user = request.args.get('user')
    database.project.create_item(project_id,name,info,user)
    return jsonify({'state':'success'})

