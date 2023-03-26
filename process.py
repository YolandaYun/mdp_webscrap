import pandas as pd
import json

# https://jsoncrack.com/editor
# https://towardsdatascience.com/all-pandas-json-normalize-you-should-know-for-flattening-json-13eae1dfb7dd

for machine in ["crawler-tractor", "wheel-loader", "rock-truck", "crawler-loader", "compactor"]:
    filename = machine + ".jsonl"
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.json_normalize(data,  meta = ['modelname', 'modelid', ['specifications', 'topparam']], record_path = ['specifications', 'subparam'])
    csv_name = machine + "_specifications.csv"
    df.to_csv(csv_name,index=False)
    print("ok")

