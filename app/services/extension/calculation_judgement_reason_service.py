from typing import List

from app.facades.nlp import cotoha, rule_base
from app.schemas.extension.dto import VerifyVoteEnrichmentDto


def execute(sentence: str):
    score = rule_base.calculation_judgement_reason(sentence=sentence)

    if not _cotoha_is_active():  # cotohaのAPIを利用しない場合、ルールベースのスコアのみ返す
        return VerifyVoteEnrichmentDto(
            rule_score=score, expected_reword_token_amount=int(score * 10)
        )

    # 文章のネガポジを判定
    sentence_emotion = cotoha.predict(sentence)
    cotoha_sentiment = sentence_emotion.get("result").get("sentiment")
    sentence_is_positive: bool = True
    if cotoha_sentiment == "Negative":
        sentence_is_positive = False

    # 感情的な単語と通常の単語の比率で、文章の客観度合いを算出する。
    emotional_phrase = sentence_emotion.get("result").get("emotional_phrase")
    emotional_keywords = [dict.get("form") for dict in emotional_phrase]

    sentence_keywords = cotoha.keyword(sentence)
    objective_weight = _objective_score_weight(
        emotional_keywords=emotional_keywords,
        sentence_keywords=sentence_keywords,
    )
    # TODO: ロジックの修正の必要あり
    objective_score = objective_weight * score
    objective_score = objective_score if objective_score > 0.1 else 0.1
    expected_reword_token_amount = int(objective_score * 10)

    return VerifyVoteEnrichmentDto(
        rule_score=score,
        high_level_analytics=True,
        sentence_is_positive=sentence_is_positive,
        sentence_keywords=sentence_keywords,
        emotional_keywords=emotional_keywords,
        objective_weight=objective_weight,
        objective_score=objective_score,
        expected_reword_token_amount=expected_reword_token_amount,
    )


def _cotoha_is_active():
    """CotohaAPIが利用可能な場合はTrue"""
    return cotoha is not None


def _objective_score_weight(
    emotional_keywords: List[str],
    sentence_keywords: List[str],
):
    if len(sentence_keywords) == 0 and len(sentence_keywords) == 0:
        return 0.1
    object_words_rate = len(sentence_keywords) / (
        len(emotional_keywords) + len(sentence_keywords)
    )
    sentence_len_weight = 0.1
    if object_words_rate > 0.7:
        weight = 1
    elif object_words_rate > 0.5:
        weight = 0.8
    elif object_words_rate > 0.3:
        weight = 0.5

    return weight
