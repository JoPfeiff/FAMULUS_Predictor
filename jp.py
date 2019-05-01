from cassis import *

import json

SENTENCE_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence"
TOKEN_TYPE = "de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token"

with open('req.json',) as f:
    json_object = json.load(f)

metadata = json_object["metadata"]

layer = metadata["layer"] # Ergebnis
feature = metadata["feature"] # Feature
projectId = metadata["projectId"]
document = json_object["document"]

xmi = document["xmi"]
documentId = document["documentId"]
userId = document["userId"]
typesystem_raw = json_object["typeSystem"]

typesystem = load_typesystem(typesystem_raw)
cas = load_cas_from_xmi(xmi, typesystem=typesystem)

for sentence in cas.select(SENTENCE_TYPE):
    tokens = [e for e in cas.select_covered(TOKEN_TYPE, sentence)]
    token_texts = [cas.get_covered_text(e) for e in tokens]

AnnotationType = typesystem.get_type(layer)

# Predict stuff
predictions = [(0, 1, "dafür", "ADHS")]
for prediction in predictions:
    fields = {'begin': tokens[prediction[0]].begin,
              'end': tokens[prediction[1] - 1].end,
              feature: prediction[2]
              }
    annotation = AnnotationType(**fields)
    cas.add_annotation(annotation)

xmi = cas.to_xmi()
print(xmi)

