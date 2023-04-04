import csv
import sqlite3


# sqlite3 db
con = sqlite3.connect('iron_planet_clean_excavator.db')
cur = con.cursor()
# cur.execute('DROP TABLE bids')
cur.execute("CREATE TABLE bids (id INTEGER PRIMARY KEY, model TEXT, type TEXT, winningbid INTEGER, metersread INTEGER, year INTEGER)")



with open("iron_planet_excavator.csv", 'r') as csvf:
    reader = csv.DictReader(csvf)
    i = 0
    for row in reader:
        name = row['name'].lower()
        typee = name.split()[-2]
        model = name.split("cat")[1].split()[0]
        print("typee ", typee)
        print("model ", model)

        if (row['metersread'] == "NONE"):
            continue
        winning_bid = row['winningbid'].strip().split('$')[1]
        winning_bid = winning_bid.replace(",", "")
        winning_bid = int(winning_bid)
        
        meters_read = row['metersread'].strip().split()[0]
        meters_read = meters_read.replace(",", "")
        meters_read = int(meters_read)

        if name.split()[0].isdigit():
            year = int(name.split()[0])
            i += 1
            cur.execute("INSERT INTO bids (model, type, winningbid, metersread, year) VALUES (?, ?, ?, ?, ?)", (model, typee, winning_bid, meters_read, year))
            con.commit()
print(i)