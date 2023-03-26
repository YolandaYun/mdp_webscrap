import requests
import json

# generate a request to ritchiespecs backend to collect all model names
# frontend equivalent: eg. (https://www.ritchiespecs.com/equipment/crawler-tractor/caterpillar)
machine_types = ["crawler-tractor", "wheel-loader", "rock-truck", "crawler-loader", "compactor"]

for machine_type in machine_types:
  print(" \n\n  ---------  Starting new machine type  ---------- ")
  url = "https://api.ritchiespecs.com/api/manufacturegenericsearch"
  payload = {
    "locale": "en_us",
    "q": machine_type, # change this for other machine type
    "bn": "caterpillar", 
    "sortItem": "",
    "sortorder": "",
    "selectedParams": "",
    "defaultParams": ""
  }
  request = requests.post(url, data=payload)
  print("Requesting for ", machine_type, " status code: ", request.status_code)
  data = request.json() # a dict
  # print(data)
  slugs = []
  for model in data["modellist"]:
      slug = model["slug"]
      slugs.append(slug)
  # print("slugs: ", slugs, "\n\n")

  # generate a request for each model to get details
  # frontend equivalent: eg. (https://www.ritchiespecs.com/model/caterpillar-d6t-tier-4-interim-stage-iiib-crawler-tractor)
  url = "https://api.ritchiespecs.com/api/itemdetails/model" # query string: ?locale=en_us&q=caterpillar-d6t-tier-4-interim-stage-iiib-crawler-tractor
  counter = 0
  file_name = machine_type + ".jsonl"
  all_data = []
  with open(file_name, 'w', encoding='utf-8') as f:
    for slug in slugs:
        parameters = {"locale":"en_us", "q":slug}
        request = requests.get(url, params=parameters)
        data = request.json()
        all_data.append(json.dumps(data))
    text = "\n".join(all_data)
    f.write(text)
      

# import requests
# import json
# import sqlite3

# # create connection to sqlite
# connection = sqlite3.connect('ritchiespecs.db') # create if not exist
# cursor = connection.cursor()
# cursor.execute('DROP TABLE engine_info;')
# cursor.execute('CREATE TABLE engine_info (id INTEGER PRIMARY KEY AUTOINCREMENT, modelid INTERGER, modelname TEXT, equipment_slug TEXT, engine_model TEXT);')

       
# def crawler_tractor(machine_type, data):
#   li = data["specifications"]
#   engine_model = "NOTFOUND"
#   for engine_dict in li:
#     if engine_dict["topparam"] == "Engine":
#       subparam = engine_dict["subparam"] # a list
#       for dic in subparam:
#         # if dic["subparam"] == "Engine Make":
#         #   engine_make = dic["value1"]
#         if dic["subparam"] == "Engine Model":
#           engine_model = dic["value1"]
#         # if dic["subparam"] == "Gross Power":
#         #   gross_power_hp = dic["value1"]
#         # if dic["subparam"] == "Net Power":
#         #   net_power_hp = dic["value1"]
#         # if dic["subparam"] == "Displacement":
#         #   displacement_cu_in = dic["value1"]
      
#   cursor.execute('INSERT INTO engine_info (modelid, modelname, equipment_slug, engine_model) VALUES (?,?,?,?)', 
#                 (data["modelid"], data["modelname"], data["equipment_slug"],engine_model)
#                 )
#   connection.commit()
#   # (data["modelid"], data["modelname"], data["equipment_slug"],engine_make, engine_model, gross_power_hp, net_power_hp, displacement_cu_in)


# # generate a request to ritchiespecs backend to collect all model names
# # frontend equivalent: eg. (https://www.ritchiespecs.com/equipment/crawler-tractor/caterpillar)
# machine_types = ["crawler-tractor", "wheel-loader", "rock-truck", "crawler-loader", "compactor"]
# # 
# for machine_type in machine_types:
#   print(" \n\n  ---------  Starting new machine type  ---------- ")
#   url = "https://api.ritchiespecs.com/api/manufacturegenericsearch"
#   payload = {
#     "locale": "en_us",
#     "q": machine_type, # change this for other machine type
#     "bn": "caterpillar", 
#     "sortItem": "",
#     "sortorder": "",
#     "selectedParams": "",
#     "defaultParams": ""
#   }
#   request = requests.post(url, data=payload)
#   print("Requesting for ", machine_type, " status code: ", request.status_code)
#   data = request.json() # a dict
#   # print(data)
#   slugs = []
#   for model in data["modellist"]:
#       slug = model["slug"]
#       slugs.append(slug)
#   # print("slugs: ", slugs, "\n\n")

#   # generate a request for each model to get details
#   # frontend equivalent: eg. (https://www.ritchiespecs.com/model/caterpillar-d6t-tier-4-interim-stage-iiib-crawler-tractor)
#   url = "https://api.ritchiespecs.com/api/itemdetails/model" # query string: ?locale=en_us&q=caterpillar-d6t-tier-4-interim-stage-iiib-crawler-tractor
#   counter = 0
#   # file_name = machine_type + ".json"
#   # with open(file_name, "w") as outfile:
#   with open("nothing.txt", "w") as outfile:
#     for slug in slugs:
#         parameters = {"locale":"en_us", "q":slug}
#         request = requests.get(url, params=parameters)
#         data = request.json()
#         crawler_tractor(machine_type, data)
#         # str_json = json.dumps(data, indent=2)
#         # outfile.write(str_json)
#   connection.commit()
 