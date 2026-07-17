import pytest

from mkfilename import make_filename

test_data = [
    (
        "Mit <dies/en> 'Mitteln'*: jagen Katzen weniger \"Vögel\" & Mäuse _ (1);",
        "mit_diesen_mitteln_jagen_katzen_weniger_voegel_and_maeuse_1",
    ),
    (
        """
Sunday Cruise
von
Elmar Frey feat. Roberto Bossard| Elmar Frey| Mark Soskin| Roberto Bossard
""",
        "sunday_cruise_von_elmar_frey_feat_roberto_bossard_elmar_frey_mark_soskin_roberto_bossard",
    ),
    (
        "Bald, bald isch Wienacht.mscz",
        "bald_bald_isch_wienacht.mscz",
    ),
    # capital umlauts
    ("Ärger", "aerger"),
    ("Öl", "oel"),
    ("Über", "ueber"),
    # sharp s
    ("Straße", "strasse"),
    ("Weiß", "weiss"),
    # lowercasing
    ("ABC", "abc"),
    ("CamelCase", "camelcase"),
    # the extension is part of the filename and folds too
    ("Foo.PDF", "foo.pdf"),
    (
        "Ihre OrellFüssli-Rechnung Nr. 1234.PDF",
        "ihre_orellfuessli_rechnung_nr_1234.pdf",
    ),
    # dots: a trailing extension separator survives, the rest become "_"
    ("a.b.c.d", "a_b_c.d"),
    ("Dr. No", "dr_no"),
    ("...", "untitled"),
    ("no dots here", "no_dots_here"),
    # a trailing dot is not an extension separator; the "_" it becomes is stripped
    ("foo.", "foo"),
    # what follows the last dot must be alphanumeric to count as an extension;
    # here it is not, so every dot becomes "_"
    ("foo.bar baz", "foo_bar_baz"),
    # but a bare "foo.bar" is indistinguishable from stem+extension, so it stays
    ("foo.bar", "foo.bar"),
    ("version 1.2.3", "version_1_2.3"),
    # a dot that already had a space after it yields "__", which the _+ collapse
    # merges back to one - so these are unchanged by the replace-vs-drop choice
    ("Nr. 1234.PDF", "nr_1234.pdf"),
    # $ -> S must still end up lowercase
    ("$", "s"),
    ("5$ bill", "5s_bill"),
    # NFKD can *produce* a translatable char: fullwidth $ decomposes to "$",
    # which the second translate turns into "S". Guards .lower() placement:
    # it must run after that translate, not before.
    ("＄", "s"),
    ("！", "untitled"),
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
