"""Check the Kurdish letter table against real Kurdish fonts.

Kurdish fonts such as Sarchia and Unikurd Web draw some contextual forms
from private-use code points (U+E000-U+E009) or from presentation-form code
points they use in their own way, and they leave out many standard
presentation forms. ``LETTERS_KURDISH`` has to match those fonts, and a test
on strings alone cannot show that the right glyph appears on screen.

This test uses the font itself. These fonts also have OpenType (GSUB) rules
that pick the right contextual glyph for the plain Unicode letter. For every
letter and every position (isolated, initial, medial, final) it checks that:

* HarfBuzz shaping the *unshaped* text with the font's own rules, and
* the font's cmap glyph for the code point arabic_reshaper outputs

give the same glyph (same glyph, or an identical outline and advance width).

Put Kurdish fonts (for example ``85_Sarchia_Soran.ttf`` or Unikurd Web's
``Unikuweb.ttf``) anywhere under ``fonts/`` at the repository root. That
directory is git-ignored. The test runs only on fonts that use the Kurdish
private-use convention, and skips letters a font doesn't have.
"""
from pathlib import Path

import pytest

pytest.importorskip('fontTools', reason='fonttools not installed')
hb = pytest.importorskip('uharfbuzz', reason='uharfbuzz not installed')

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

from arabic_reshaper import ArabicReshaper
from arabic_reshaper.letters import FINAL, INITIAL, ISOLATED, LETTERS_KURDISH, MEDIAL

_FONTS_DIR = Path(__file__).parent.parent.parent / 'fonts'
_ALL_FONTS = sorted(
    p for ext in ('*.ttf', '*.otf') for p in _FONTS_DIR.rglob(ext)
) if _FONTS_DIR.is_dir() else []

# The Sorani Kurdish alphabet. Tested even when a letter is missing from
# LETTERS_KURDISH, so a missing entry fails instead of going unnoticed.
SORANI_ALPHABET = (
    'ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆهەیێ'
)

MEEM = 'م'  # dual-joining neighbour present in every Arabic-script font
FORM_NAMES = {ISOLATED: 'isolated', INITIAL: 'initial',
              MEDIAL: 'medial', FINAL: 'final'}


def _contexts(letter):
    """(form, text, index of the letter in the text) for every position."""
    return [
        (ISOLATED, letter, 0),
        (INITIAL, letter + MEEM, 0),
        (MEDIAL, MEEM + letter + MEEM, 1),
        (FINAL, MEEM + letter, 1),
    ]


def _is_kurdish_pua_font(cmap):
    # Kurdish fonts put the final form of AE (U+06D5) at U+E000.
    return 0x06D5 in cmap and 0xE000 in cmap


def _collect_cases():
    cases = []
    letters = sorted(set(LETTERS_KURDISH) | set(SORANI_ALPHABET))
    for path in _ALL_FONTS:
        cmap = TTFont(str(path), lazy=True).getBestCmap() or {}
        if not _is_kurdish_pua_font(cmap):
            continue
        for letter in letters:
            if ord(letter) not in cmap:
                continue
            for form, text, index in _contexts(letter):
                cases.append(pytest.param(
                    path, letter, form, text, index,
                    id=f'{path.stem}-U+{ord(letter):04X}-{FORM_NAMES[form]}',
                ))
    return cases


_CASES = _collect_cases()


class _Font:
    _cache = {}

    @classmethod
    def load(cls, path):
        if path not in cls._cache:
            cls._cache[path] = cls(path)
        return cls._cache[path]

    def __init__(self, path):
        self.name = path.name
        self.tt = TTFont(str(path))
        self.cmap = self.tt.getBestCmap()
        self.order = self.tt.getGlyphOrder()
        self.glyph_set = self.tt.getGlyphSet()
        self.hb_font = hb.Font(hb.Face(hb.Blob.from_file_path(str(path))))

    def shaped_glyph_at(self, text, index):
        """Glyph name HarfBuzz picks for the character at ``index``."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        # Turn off optional ligatures so every character keeps its own glyph.
        hb.shape(self.hb_font, buf, {'liga': False, 'dlig': False})
        names = [self.order[info.codepoint]
                 for info in buf.glyph_infos if info.cluster == index]
        assert len(names) == 1, (
            f'{self.name}: expected one glyph for {text!r}[{index}], got {names}'
        )
        return names[0]

    def signature(self, glyph_name):
        pen = RecordingPen()
        self.glyph_set[glyph_name].draw(pen)
        return self.tt['hmtx'][glyph_name][0], pen.value

    def same_glyph(self, a, b):
        return a == b or self.signature(a) == self.signature(b)


@pytest.fixture(scope='module')
def reshaper():
    return ArabicReshaper(configuration={
        'language': 'Kurdish',
        'support_ligatures': False,
    })


@pytest.mark.skipif(
    not _CASES,
    reason='No Kurdish font (with U+06D5 and U+E000) found under fonts/',
)
@pytest.mark.parametrize('font_path, letter, form, text, index', _CASES)
def test_letter_form_matches_font(font_path, reshaper, letter, form, text,
                                  index):
    font = _Font.load(font_path)
    expected_glyph = font.shaped_glyph_at(text, index)

    reshaped = reshaper.reshape(text)
    assert len(reshaped) == len(text), repr(reshaped)
    out_char = reshaped[index]
    mapped_glyph = font.cmap.get(ord(out_char))

    if mapped_glyph is not None and font.same_glyph(mapped_glyph, expected_glyph):
        return

    if form != ISOLATED and expected_glyph == font.cmap[ord(letter)]:
        # The font keeps the plain glyph here, so it defines no contextual
        # form for this letter and says nothing about what the right one is.
        pytest.skip(f'{font.name} has no {FORM_NAMES[form]} form '
                    f'for U+{ord(letter):04X}')

    assert mapped_glyph is not None, (
        f'{font.name}: reshaper outputs U+{ord(out_char):04X} for {text!r}, '
        f'which the font has no glyph for; the font uses {expected_glyph!r}'
    )
    pytest.fail(
        f'{font.name}: reshaper outputs U+{ord(out_char):04X} '
        f'({mapped_glyph!r}) for {text!r}, but the font uses {expected_glyph!r}'
    )
