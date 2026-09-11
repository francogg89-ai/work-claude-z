from probe.launch import prepare


def test_fresh_prepare_creates_a_new_strong_token_and_empty_database(tmp_path):
    (tmp_path / "probe.sqlite").write_text("old")
    token = prepare(tmp_path, fresh=True)
    assert len(token) >= 32
    assert (tmp_path / "token").read_text() == token
    assert not (tmp_path / "probe.sqlite").exists()


def test_resume_keeps_the_existing_token(tmp_path):
    first = prepare(tmp_path, fresh=True)
    assert prepare(tmp_path, fresh=False) == first


def test_fresh_prepare_never_reuses_the_previous_token(tmp_path):
    assert prepare(tmp_path, fresh=True) != prepare(tmp_path, fresh=True)
