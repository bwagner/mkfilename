import pytest

from mkfilename import make_filename

test_data = [
    (
        "Mit <dies/en> 'Mitteln'*: jagen Katzen weniger \"Vögel\" & Mäuse _ (1);",
        "Mit_diesen_Mitteln_jagen_Katzen_weniger_Voegel_and_Maeuse_1",
    ),
    (
        """
Sunday Cruise
von
Elmar Frey feat. Roberto Bossard| Elmar Frey| Mark Soskin| Roberto Bossard
""",
        "Sunday_Cruise_von_Elmar_Frey_feat._Roberto_Bossard_Elmar_Frey_Mark_Soskin_Roberto_Bossard",
    ),
    (
        "Bald, bald isch Wienacht.mscz",
        "Bald_bald_isch_Wienacht.mscz",
    ),
    # capital umlauts
    ("Ärger", "Aerger"),
    ("Öl", "Oel"),
    ("Über", "Ueber"),
    # sharp s
    ("Straße", "Strasse"),
    ("Weiß", "Weiss"),
    # leading/trailing underscores after substitution
    ("___foo___", "foo"),
    (" - hello - ", "hello"),
    # empty fallback
    ("", "untitled"),
    ("   ", "untitled"),
    ("!!!", "untitled"),
    ("😀", "untitled"),
    # length cap at 255
    ("a" * 300, "a" * 255),
    # leading dot
    (".foo", "_foo"),
    (".bashrc", "_bashrc"),
    # carriage return
    ("a\rb", "a_b"),
    # en/em dash
    ("foo–bar", "foo_bar"),
    ("foo—bar", "foo_bar"),
    # English &
    ("foo & bar", "foo_and_bar"),
]


@pytest.mark.parametrize("test_input, expected", test_data)
def test_make_filename(test_input, expected):
    assert make_filename(test_input) == expected
