from history.history import History
from responses import welcome, goodbyes

responses = {
    "welcome": welcome.process_response(),
    "goodbyes": goodbyes.process_response()
}

learning = False
learning_input = ""


def process_response(classifier):
    global learning
    global learning_input

    _class = History.get_most_recent()["classification"]
    prob = History.get_most_recent()["probability"]
    inp = History.get_most_recent()["input"]

    if learning:
        if inp in responses.keys():
            classifier.submit_document(learning_input, inp)
            classifier.fit()
        learning = False
        return "Learned"

    if prob < 0.75:
        learning = True
        learning_input = inp
        return "I didn't understand, is that a thing of the following? " + str(list(responses.keys()))

    return responses[_class]
