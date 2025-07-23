from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017")

# Выбор базы данных
db = client['myDatabase']

# Выбор коллекции
checklists_collection = db['checklists']

# Получение всех чек-листов
checklists = checklists_collection.find()

# Вывод чек-листов и их составляющих
for checklist in checklists:
    print(f"Чек-лист: {checklist['name']}")
    for item in checklist.items():
        print(item[1])
    print("\n")