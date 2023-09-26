import json
import requests

#получение файла перестановок с API
with open("./Data/replacement.json", "r") as read_file:
    replacements = json.load(read_file)
#получение перестановок без повторений. Вносится последнее изменение
replacements.reverse()
replacementSet = []
[replacementSet.append(x) for x in replacements if x not in replacementSet]
del replacements, read_file

#получение файла сообщений из директории проекта Data
dataText = requests.get("https://raw.githubusercontent.com/thewhitesoft/student-2023-assignment/main/data.json")
data = json.loads(dataText.text)
del dataText

for rep in replacementSet:

    # если сообщения изночально не было
    if rep['source'] == None:
        #удаление всех вставленых сообщений
        data = [i for i in data if i != rep['replacement']]
    
    for message in data:
        #если перестановка найдена в сообщении
        if message.find(rep['replacement']) != -1:
            #исправление сообщения
            data.insert(data.index(message), message.replace(rep['replacement'], rep['source']))
            data.remove(message)

#запись исправленных сообщений в файл result.json в директорию проекта Data
with open("./Data/result.json", "w") as write_file:
    json.dump(data, write_file, indent=2)
