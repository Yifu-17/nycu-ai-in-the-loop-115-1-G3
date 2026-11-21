from whychanged.diff_parser import compare_dicts, flatten, parse_env, parse_settings


def test_flatten_nested_yaml():
    data = {"train": {"lr": 0.001, "layers": [1, 2]}, "seed": 42}
    assert flatten(data) == {"train.lr": "0.001", "train.layers": "[1, 2]", "seed": "42"}


def test_parse_env_skips_comments_and_quotes():
    text = '# comment\nexport A=1\nB="two"\n\nbad line\n'
    assert parse_env(text) == {"A": "1", "B": "two"}


def test_compare_finds_changed_added_removed():
    before = {"lr": "0.001", "dropout": "0.1", "old": "x"}
    after = {"lr": "0.0005", "dropout": "0.1", "new": "y"}
    changes = {c.key: (c.old, c.new) for c in compare_dicts(before, after, "f.yaml")}
    assert changes == {"lr": ("0.001", "0.0005"), "old": ("x", None), "new": (None, "y")}


def test_reordered_yaml_is_not_a_change():
    a = parse_settings("c.yaml", "lr: 1\nbs: 2\n")
    b = parse_settings("c.yaml", "# moved\nbs: 2\nlr: 1\n")
    assert compare_dicts(a, b, "c.yaml") == []


def test_missing_file_counts_as_empty():
    assert parse_settings("c.yaml", None) == {}
