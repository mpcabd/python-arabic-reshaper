import pytest
from pathlib import Path

pytest.importorskip('fontTools', reason='fonttools not installed')

from fontTools.ttLib import TTFont
from arabic_reshaper import ArabicReshaper
from arabic_reshaper.letters import LETTERS_ARABIC, ISOLATED
from arabic_reshaper.ligatures import LIGATURES
from arabic_reshaper.reshaper_config import config_for_true_type_font

_FONTS_DIR = Path(__file__).parent.parent.parent / 'fonts'
_FONT_FILES = sorted(_FONTS_DIR.rglob('*.otf')) if _FONTS_DIR.is_dir() else []


def _expected_config(font_path: Path) -> dict:
    """Independently compute the config config_for_true_type_font should return.

    Uses fonttools directly to build the expected output so that the test is a
    genuine check of correctness, not just a smoke test.
    """
    ttfont = TTFont(str(font_path))
    cmap_chars: set[int] = set()
    for table in ttfont['cmap'].tables:
        cmap_chars.update(table.cmap.keys())

    has_isolated = all(
        ord(v[ISOLATED]) in cmap_chars
        for v in LETTERS_ARABIC.values()
    )

    expected: dict = {'use_unshaped_instead_of_isolated': not has_isolated}

    for name, (_, forms_tuple) in LIGATURES:
        forms = [f for f in forms_tuple if f]
        # A ligature is enabled when every non-empty form glyph is in the font.
        # If there are no non-empty forms (degenerate entry), treat as enabled.
        expected[name] = not forms or all(ord(f) in cmap_chars for f in forms)

    return expected


@pytest.mark.skipif(not _FONT_FILES, reason='No .otf files found under fonts/')
class TestFontConfig:
    @pytest.mark.parametrize('font_path', _FONT_FILES, ids=lambda p: p.stem)
    def test_config_matches_font_capabilities(self, font_path):
        assert config_for_true_type_font(str(font_path)) == _expected_config(font_path)

    @pytest.mark.parametrize('font_path', _FONT_FILES, ids=lambda p: p.stem)
    def test_config_produces_working_reshaper(self, font_path):
        config = config_for_true_type_font(str(font_path))
        reshaper = ArabicReshaper(configuration=config)
        assert reshaper.reshape('السلام عليكم')
