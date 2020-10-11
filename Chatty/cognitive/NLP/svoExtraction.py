import spacy


def find_recursive(token, dep, chunks):
    children = token.children
    spans = []

    for c in children:
        if c.dep_ == dep:
            for chunk in chunks:
                if c in chunk:
                    spans.append(chunk.string)
                    break

        spans.extend(find_recursive(c, dep, chunks))

    return spans


def get_predicates(sent):
    predicates = []
    for token in sent:
        if token.pos_ in ("VERB", "AUX"):
            predicates.append(token)
    return predicates


def get_subjects(predicates):
    subjects = []
    for pred, predicate in enumerate(predicates):
        subjects.append([])
        for rel in predicate.children:
            if rel.dep_ in ("nsubj",):
                if rel.pos_ == "PRON":
                    subjects[pred].extend(subjects[pred - 1] if subjects[pred - 1] else [rel])
                else:
                    subjects[pred].append(rel)
    return subjects


def get_objects(predicates, sent):
    spans = list(sent.ents) + list(sent.noun_chunks)  # collect nodes
    spans = spacy.util.filter_spans(spans)

    objects = []
    for pred, predicate in enumerate(predicates):
        modifiers = []
        if predicate.dep_ == "amod":
            modifiers.append(predicate.head)

        objects.append(modifiers)
        for rel in predicate.children:
            if rel.dep_ in ("dobj", "pobj", "attr") and rel.pos_ not in ("NUM",):
                obj = rel
                for span in spans:
                    if rel.text in span.string:
                        obj = span
                        break

                objects[pred].extend(find_recursive(obj[len(obj) - 1], "conj", spans))
                objects[pred].append(obj.string)
            if rel.dep_ in ("prep",):
                for c in rel.children:
                    if c.pos_ in ("NUM",):
                        continue
                    for span in spans:
                        if c.text in span.string:
                            objects[pred].append(span)
                            break
            if rel.dep_ in ("acomp", ):
                for c1 in rel.children:
                    if c1.dep_ in ("prep",):
                        for c2 in c1.children:
                            if c2.pos_ in ("NUM",):
                                continue
                            for span in spans:
                                if c2.text in span.string:
                                    objects[pred].append(rel.text + " " + c1.text + " " + span.string)
                                    break
    return objects


def get_svo_sent(sent):
    pred = get_predicates(sent)
    subj = get_subjects(pred)
    objs = get_objects(pred, sent)

    svo = []

    lasts = []
    lasto = []
    for ss, p, os in zip(subj, pred, objs):
        if ss:
            lasts = ss
        if not os:
            continue
        if ss:
            for s in ss:
                for o in os:
                    svo.append((str(s).strip(), str(p).strip(), str(o).strip()))
        else:
            for s in (lasto if lasto else lasts):
                for o in os:
                    svo.append((str(s).strip(), str(p).strip(), str(o).strip()))
        lasto = os
    return svo