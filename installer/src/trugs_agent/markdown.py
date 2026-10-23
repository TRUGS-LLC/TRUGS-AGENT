"""Extract fenced blocks using CommonMark container and indentation rules."""

from markdown_it import MarkdownIt


def blocks(text):
    for token in MarkdownIt("commonmark").parse(text):
        if token.type != "fence":
            continue
        # CommonMark permits an implicit closer at EOF or a container boundary.
        # Instructions retain the kit's stricter requirement for an explicit one.
        start, end = token.map
        if end - start != token.content.count("\n") + 2:
            raise ValueError(f"unclosed fenced block at line {start + 1}")
        info = token.info.split()
        yield info[0] if info else "", token.content
