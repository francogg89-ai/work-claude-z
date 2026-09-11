import pytest

from probe.url import clear, copy_url


def test_copy_puts_the_url_on_the_clipboard_without_returning_or_printing_it(tmp_path, capsys):
    (tmp_path / "chatgpt-url.txt").write_text("https://h.example/mcp/" + "t" * 43)
    clipboard = []
    result = copy_url(tmp_path, invalid=False, copier=clipboard.append)
    assert clipboard == ["https://h.example/mcp/" + "t" * 43]
    assert result is None
    assert "t" * 43 not in capsys.readouterr().out


def test_copy_invalid_uses_the_invalid_url_file(tmp_path):
    (tmp_path / "chatgpt-url-invalida.txt").write_text("https://h.example/mcp/" + "u" * 43)
    clipboard = []
    copy_url(tmp_path, invalid=True, copier=clipboard.append)
    assert clipboard == ["https://h.example/mcp/" + "u" * 43]


def test_copy_refuses_when_the_exposure_was_not_certified(tmp_path):
    with pytest.raises(SystemExit):
        copy_url(tmp_path, invalid=False, copier=lambda _: None)


def test_clear_overwrites_the_clipboard_with_an_empty_value():
    clipboard = ["secret"]
    clear(copier=lambda value: clipboard.__setitem__(0, value))
    assert clipboard == [""]
