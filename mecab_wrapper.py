
from MeCab import Tagger

def mecab_parse(text):
    tagger = Tagger('-Ochasen')
    node = tagger.parseToNode(text)
    result = []
    while node:
        feature = node.feature.split(',')
        result.append({
            "surface": node.surface,
            "pos": feature[0],
            "pos1": feature[1],
            "pos2": feature[2],
            "pos3": feature[3],
            "conjugated_type": feature[4],
            "conjugated_form": feature[5],
            "base": feature[6]
        })
        node = node.next
    return result