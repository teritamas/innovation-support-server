def calculation_judgement_reason(sentence: str) -> float:
    """投票理由のスコアを[0-1]の範囲で返す"""

    sentence_len_weight = _calculation_sentence_len_weight(sentence)
    finalize_score = sentence_len_weight * 1
    return finalize_score if finalize_score <= 1 else 1


def _calculation_sentence_len_weight(sentence):
    sentence_len_weight = 0
    if len(sentence) > 200:
        sentence_len_weight = 2
    elif len(sentence) > 100:
        sentence_len_weight = 1.5
    elif len(sentence) > 50:
        sentence_len_weight = 1.2
    return sentence_len_weight
