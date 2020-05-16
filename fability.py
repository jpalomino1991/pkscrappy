
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

with open('ability.csv', "r", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column name are {", ".join(row)}')
            line_count += 1
        else:
            #print(row[0] + " " + row[1])
            doc_ref = db.collection(u'Ability').document(row[0])

            data = {
                'Name': row[0],
                'Description': row[1],
            }
            batch.set(doc_ref, data)

            if line_count == 500:
                batch.commit()
                line_count = 0

            line_count += 1
    batch.commit()
    print(f'Processed {line_count} lines.')
