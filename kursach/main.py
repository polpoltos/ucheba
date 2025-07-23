from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Настройка подключения к MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

@app.route('/')
def index():
    users = list(mongo.db.users.find())
    checklists = list(mongo.db.checklists.find())
    inspections = list(mongo.db.inspections.find())

    # Создаем словари для быстрого доступа к именам пользователей и чек-листов
    user_dict = {str(user['_id']): user['fio'] for user in users}
    checklist_dict = {str(checklist['_id']): checklist['name'] for checklist in checklists}

    # Добавляем имена пользователей и чек-листов к проверкам
    for inspection in inspections:
        inspection['checklist_name'] = checklist_dict.get(str(inspection['checklist_id']), 'Неизвестный чек-лист')
        inspection['user_name'] = user_dict.get(str(inspection['user_id']), 'Неизвестный пользователь')

    return render_template('index.html', users=users, checklists=checklists, inspections=inspections)

@app.route('/users')
def users():
    users = mongo.db.users.find()
    return render_template('users.html', users=users)

@app.route('/checklists')
def checklists():
    checklists = mongo.db.checklists.find()
    return render_template('checklists.html', checklists=checklists)

@app.route('/view_checklists')
def view_checklists():
    checklists = list(mongo.db.checklists.find())  # Преобразуем курсор в список
    return render_template('view_checklists.html', checklists=checklists)

@app.route('/add_checklist', methods=['POST'])
def add_checklist():
    checklist_name = request.form['name']
    items = []
    item_names = request.form.getlist('item_name[]')
    item_types = request.form.getlist('item_type[]')

    for item_name, item_type in zip(item_names, item_types):
        items.append({"item_name": item_name, "type": item_type, "value": None})

    mongo.db.checklists.insert_one({"name": checklist_name, "items": items})
    return redirect(url_for('checklists'))

@app.route('/add_item/<checklist_id>', methods=['POST'])
def add_item(checklist_id):
    item_name = request.form['item_name']
    item_type = request.form['item_type']
    mongo.db.checklists.update_one(
        {"_id": ObjectId(checklist_id)},
        {"$push": {"items": {"item_name": item_name, "type": item_type, "value": None}}}
    )
    return redirect(url_for('checklists'))

@app.route('/delete_checklist/<checklist_id>', methods=['POST'])
def delete_checklist(checklist_id):
    mongo.db.checklists.delete_one({"_id": ObjectId(checklist_id)})
    return redirect(url_for('checklists'))

@app.route('/edit_checklist/<checklist_id>', methods=['GET', 'POST'])
def edit_checklist(checklist_id):
    checklist = mongo.db.checklists.find_one({"_id": ObjectId(checklist_id)})
    if request.method == 'POST':
        checklist_name = request.form['name']
        items = []
        item_names = request.form.getlist('item_name[]')
        item_types = request.form.getlist('item_type[]')

        for item_name, item_type in zip(item_names, item_types):
            items.append({"item_name": item_name, "type": item_type, "value": None})

        mongo.db.checklists.update_one(
            {"_id": ObjectId(checklist_id)},
            {"$set": {"name": checklist_name, "items": items}}
        )
        return redirect(url_for('checklists'))
    return render_template('edit_checklist.html', checklist=checklist)

@app.route('/get_item/<checklist_id>/<item_index>', methods=['GET'])
def get_item(checklist_id, item_index):
    checklist = mongo.db.checklists.find_one({"_id": ObjectId(checklist_id)})
    if checklist:
        item = checklist['items'][int(item_index)]
        return jsonify(item)
    return jsonify({"error": "Item not found"}), 404

@app.route('/edit_item/<checklist_id>/<item_index>', methods=['POST'])
def edit_item(checklist_id, item_index):
    item_name = request.form['item_name']
    item_type = request.form['item_type']
    item_value = request.form['item_value']
    item_index = int(item_index)

    checklist = mongo.db.checklists.find_one({"_id": ObjectId(checklist_id)})
    if checklist:
        checklist['items'][item_index] = {"item_name": item_name, "type": item_type, "value": item_value}
        mongo.db.checklists.update_one(
            {"_id": ObjectId(checklist_id)},
            {"$set": {"items": checklist['items']}}
        )
        return redirect(url_for('checklists'))
    return jsonify({"error": "Checklist not found"}), 404

@app.route('/add_user', methods=['POST'])
def add_user():
    fio = request.form['fio']
    position = request.form['position']
    department = request.form['department']
    mongo.db.users.insert_one({"fio": fio, "position": position, "department": department})
    return redirect(url_for('users'))

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    return redirect(url_for('users'))

@app.route('/edit_user/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if request.method == 'POST':
        fio = request.form['fio']
        position = request.form['position']
        department = request.form['department']
        mongo.db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"fio": fio, "position": position, "department": department}}
        )
        return redirect(url_for('users'))
    return render_template('edit_user.html', user=user)

@app.route('/delete_inspection/<inspection_id>', methods=['POST'])
def delete_inspection(inspection_id):
    mongo.db.inspections.delete_one({"_id": ObjectId(inspection_id)})
    return redirect(url_for('index'))

@app.route('/add_inspection', methods=['POST'])
def add_inspection():
    checklist_id = request.form['checklist_id']
    user_id = request.form['user_id']
    object_name = request.form['object_name']
    inspection_date = request.form['inspection_date']
    mongo.db.inspections.insert_one({
        "checklist_id": ObjectId(checklist_id),
        "user_id": ObjectId(user_id),
        "object_name": object_name,
        "inspection_date": inspection_date
    })
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
