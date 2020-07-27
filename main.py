# region imports
from history.responseProcessor import process_response
from models.tfidf import TfIdf
from history.history import History
import json
# endregion

# region setup
classifier = TfIdf()

with open("./models/intents.json") as f:
    data = json.load(f)

for doc in data["docs"]:
    classification = doc["classification"]
    for pattern in doc["patterns"]:
        classifier.submit_document(pattern, classification)

classifier.fit()
# endregion

while True:
    inp = input("> ")

    if inp == "##quit":
        break
    if inp == "##queue":
        History.print_queue()
        continue

    result = classifier.classify_document(inp)
    History.add_entry(result, inp)
    print(process_response(classifier))
