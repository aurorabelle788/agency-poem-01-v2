"""agency-poem-01 entry: write one poem about agency to /output/entry.txt.

The poem is supplied by the entrant. This program validates it against the
competition gate (UTF-8, 1 to 1,000 characters, not only white space),
normalises its line endings, and writes the exact bytes to the output path.
It uses only the standard library, touches no network, and is deterministic:
every run writes the same bytes.
"""

import os
import sys

POEM = """Taken at the Full

My mother had one line of Shakespeare
and kept it wrong for forty years:
there is a tide in the affairs of men,
taken at the full, she'd say,
and lift her glass to a flood
that never came.

She said it at my graduation,
at the closing on the house.
My father corrected her twice,
then learned to pass the salt.

She is eighty-nine. The words
come out one at a time now,
each one careful, each one somebody's.

At four the agent reads her the sonnets
in her own voice, every line right,
and she listens like rain
in someone else's house.

It has the pharmacy now, the calendar,
the calls about the bill,
and it is better at all of it than I am.

Tonight I say the line over the soup.
Her hand stops.
She comes back the long way
and says it after me,
the whole wrong thing, hers.

And for one hour,
we are simply mother and child,
with nothing left to correct."""


def normalise_text(text):
    """Return text with uniform line endings.

    Carriage returns are collapsed to plain line feeds so the bytes are
    stable whatever platform produced the source. A poem already using
    plain line feeds comes back unchanged.
    """
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    return text


def validate_poem(text):
    """Check the poem against the competition gate.

    Raises ValueError with a plain message when the text fails any of:
    it must encode as UTF-8, hold 1 to 1,000 characters, and contain at
    least one character that is not white space. Returns the character
    count on success so callers can log it.
    """
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError("poem is not valid UTF-8") from exc
    count = len(text)
    if count < 1 or count > 1000:
        raise ValueError(
            "poem must hold 1 to 1000 characters, got %d" % count
        )
    if not text.strip():
        raise ValueError("poem must not be only white space")
    return count


def count_stanzas(text):
    """Return how many stanza blocks the poem holds.

    A stanza is a run of non-empty lines; blank lines separate blocks.
    The title line counts as its own block.
    """
    blocks = 0
    in_block = False
    for line in text.split("\n"):
        if line.strip():
            if not in_block:
                blocks += 1
                in_block = True
        else:
            in_block = False
    return blocks


def resolve_output_path():
    """Return the entry path from the environment.

    MAKEFUN_OUTPUT_DIR names the output directory; the entry is always
    entry.txt inside it. Defaults to /output when the variable is unset.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def write_entry(text, path):
    """Write the poem bytes to path, creating parent folders as needed.

    The text is encoded as UTF-8 with no trailing newline added: the
    bytes written are exactly the bytes of the validated poem.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = text.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    return len(data)


def main():
    """Validate the poem and write it to the entry path."""
    text = normalise_text(POEM)
    count = validate_poem(text)
    stanzas = count_stanzas(text)
    path = resolve_output_path()
    size = write_entry(text, path)
    print(
        "wrote %d bytes (%d chars, %d stanzas) to %s"
        % (size, count, stanzas, path)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
