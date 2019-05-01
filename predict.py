from flair.data import Sentence
from flair.models import SequenceTagger
from pathlib import Path

from nltk import sent_tokenize

# tagger: SequenceTagger = SequenceTagger.load('ner')

base_path = Path('resources/taggers/famulus_test_w_bert')

tagger = SequenceTagger.load_from_file(base_path / 'best-model.pt')


text = 'ADS ) Begründung: Frühere Diagnose und zutreffen der meinsten Symptome) gemixt mit Püterirenden Hormone). Herangehensweise: Es sich Professionel Diagnostizieren lassen und sich Tipps von experten holen; Unfeld Begrundet) Diagnose: Verhalten nicht konstant songern seit einiger zeit vorhanden. Hat es eine veränderung in sein unfeld gegeben? Herangehensweise : Prüfen ob es Ereignisse in der Famile gab. Freundeskreiss genauer überprufen. Bei letzteren kann es gut sein das sie ein schleichter einfluss sind, das sie so zu sagen die schelchten eigenschaften von Markus hervorbringen. '

sent_splits = sent_tokenize(text)
sent_splits = [text]

sentences = [Sentence(s) for s in sent_splits]

tagger.predict(sentences)

output_list = []

tag_dicts = ['erg_sonstiges', 'erg_schreiben', 'erg_lesen', 'erg_leistung', 'erg_emotion', 'dia_sozial', 'dia_intelligenz', 'dia_autismus', 'dia_ADHS']



for tag_dict in tag_dicts:

    start = 0
    end = 0

    sent_start = 0

    for s, sentence in enumerate(sentences):

        current_label = 'O'

        for token in sentence.tokens:

            if token.tags[tag_dict].value != 'O':
                print(token.tags[tag_dict].value)

            if token.tags[tag_dict].value != current_label:

                if current_label != 'O':
                    output_list.append([current_label, start, end])

                # else:
                start = sent_start + token.start_pos
                end = sent_start + token.end_pos

                    # current_label = token.tags[tag_dict].value


            elif token.tags[tag_dict].value == current_label and current_label != 'O':
                end = sent_start + token.end_pos

            current_label = token.tags[tag_dict].value

        if current_label != 'O':
            output_list.append([current_label, start, end])

        sent_start += len(sent_splits[s])


        # print('Analysing %s' % sentence)
        # print('\nThe following NER tags are found: \n')
        # print(sentence.to_tagged_string())

print(output_list)


