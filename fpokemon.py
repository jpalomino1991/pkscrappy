
from firebase import firebase
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate('./credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

batch = db.batch()

#attack = db.collection(u'Attack').stream()
# for doc in docs:
# print(doc.id)

with open('pokedex.csv', "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column name are {", ".join(row)}')
            line_count += 1
        else:
            #print(row[0] + " " + row[1])
            doc_ref = db.collection(u'Pokemon').document(row[0])

            data = {
                'Name': row[0],
                'Type 1': row[1],
                'Type 2': row[2],
                'Specie': row[3],
                'Height': row[4],
                'Weight': row[5],
                'Location': row[6],
                'SW Desc': row[7],
                'SH Desc': row[8],
                'Ability 1': row[9],
                'Ability 2': row[10],
                'Hidden Ability': row[11],
            }
            batch.set(doc_ref, data)

            if line_count == 500:
                batch.commit()
                line_count = 0

            line_count += 1
    batch.commit()
    print(f'Processed {line_count} lines.')
