from transformers import pipeline
from parsers.base_classes import ParserPost

THRESHOLD = 0.5

pipe = pipeline(
    task='text-classification',
    model='HellSoop/BMSTU_parser_model',
    tokenizer='FacebookAI/xlm-roberta-base'
)


def get_important_posts(posts: list[ParserPost], threshold: float = THRESHOLD) -> list[ParserPost]:
    """
    Filters posts objets that are important based on the text of the posts. Uses a text classification model.
    :param posts: list of posts objects
    :param threshold: threshold for filtering posts. It should be between 0 and 1 and is usually 0.5
    :return: filtered list of posts
    """
    posts_texts = [p.text for p in posts]
    predictions = pipe(posts_texts)

    important_posts = [post for post, pred in zip(posts, predictions) if pred['score'] >= threshold]
    return important_posts
