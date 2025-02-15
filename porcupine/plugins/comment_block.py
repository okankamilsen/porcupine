"""
If you select multiple lines in a Python file and type '#', then all selected
lines are commented out.

A different character is used in other programming languages. This can be
configured with comment_prefix in filetypes.toml.
"""
from __future__ import annotations

import re
from typing import Optional

from porcupine import get_tab_manager, menubar, tabs, textutils


def comment_or_uncomment(tab: tabs.FileTab, pressed_key: str | None = None) -> str | None:
    comment_prefix = tab.settings.get("comment_prefix", Optional[str])
    if pressed_key is not None and pressed_key != comment_prefix:
        return None

    try:
        start_index, end_index = map(str, tab.textwidget.tag_ranges("sel"))
    except ValueError:
        # nothing selected, add '#' normally
        return None

    start = int(start_index.split(".")[0])
    end = int(end_index.split(".")[0])
    if end_index.split(".")[1] != "0":
        # something's selected on the end line, let's (un)comment it too
        end += 1

    all_linenos = set(range(start, end))
    commented = {
        lineno
        for lineno, line in enumerate(
            tab.textwidget.get(f"{start}.0", f"{end}.0").splitlines(), start
        )
        # Ignore '# blah' comments because they are likely written by hand
        # But don't ignore indented '#    blah', that is most likely by this plugin
        if line.startswith(comment_prefix) and not re.match(r" [^ ]", line[len(comment_prefix) :])
    }

    with textutils.change_batch(tab.textwidget):
        if commented == all_linenos:
            # Uncomment everything
            for lineno in all_linenos:
                tab.textwidget.delete(f"{lineno}.0", f"{lineno}.{len(comment_prefix)}")
        else:
            # Comment uncommented lines
            for lineno in all_linenos - commented:
                tab.textwidget.insert(f"{lineno}.0", comment_prefix)

    # select everything on the (un)commented lines
    tab.textwidget.tag_remove("sel", "1.0", "end")
    tab.textwidget.tag_add("sel", f"{start}.0", f"{end}.0")
    return "break"


def on_new_filetab(tab: tabs.FileTab) -> None:
    tab.textwidget.bind("<Key>", (lambda event: comment_or_uncomment(tab, event.char)), add=True)


def setup() -> None:
    menubar.add_filetab_command("Edit/Comment Block", comment_or_uncomment)
    get_tab_manager().add_filetab_callback(on_new_filetab)
