from datetime import datetime, timezone
from typing import Literal
from urllib.parse import urlparse

from catleg.config import settings
from catleg.law_text_fr import find_id_in_string


def set_basic_loglevel():
    """
    Utility for setting the log level as per config -- meant to be used
    within CLI tools only.

    To use, set CATLEG_LOG_LEVEL=INFO in the environment
    or log_level in the .catleg.toml configuration file
    """
    log_level = settings.get("log_level")
    if log_level is not None:
        import logging

        logging.basicConfig(level=log_level.upper())


def article_id_or_url(candidate: str) -> str | None:
    match find_id_in_string(candidate, strict=True):
        case (_, article_id):
            assert isinstance(
                article_id, str
            )  # not sure why mypy does not infer it itself?
            return article_id
    try:
        parse_res = parse_legifrance_url(candidate)
    except ValueError:
        return None
    match parse_res:
        case ["article", article_id]:
            return article_id
    return None


def parse_legifrance_url(
    url: str,
) -> (
    tuple[Literal["article"], str]
    | tuple[Literal["article"], str, int]  # article version at a given time
    | tuple[Literal["section"], str, str]
):
    """
    Parse a Legifrance URL, see if it matches an article or a section of a code,
    and return the corresponding type and identifier(s).
    """
    parsed_url = urlparse(url)
    if parsed_url.hostname != "www.legifrance.gouv.fr":
        raise ValueError("Unrecognized host", parsed_url.hostname)

    path_elems = parsed_url.path.split("/")[1:]
    path_elems = [e for e in path_elems if e]  # remove empty path segments

    match path_elems:
        case ["codes", "article_lc", article_id]:
            return "article", article_id
        case ["codes", "article_lc", article_id, at_time]:
            dt = datetime.fromisoformat(at_time).replace(tzinfo=timezone.utc)
            timestamp = int(dt.timestamp() * 1000)
            return "article", article_id, timestamp
        case [
            "codes",
            "section_lc",
            text_id,
            section_id,
            *_,
        ]:  # ignore anchors in sections
            return "section", text_id, section_id
        case _:
            raise ValueError("Could not parse URL", url)
