"""Extract fenced blocks using CommonMark container and indentation rules."""

from markdown_it import MarkdownIt


def tokens(text):
    parsed = MarkdownIt("commonmark").parse(text)
    for token in parsed:
        if token.type != "fence":
            continue
        # CommonMark permits an implicit closer at EOF or a container boundary.
        # Instructions retain the kit's stricter requirement for an explicit one.
        start, end = token.map
        if end - start != token.content.count("\n") + 2:
            raise ValueError(f"unclosed fenced block at line {start + 1}")
    return parsed


def blocks(text):
    for token in tokens(text):
        if token.type == "fence":
            info = token.info.split()
            yield info[0] if info else "", token.content
