from unittest.mock import mock_open, patch

from generators.base import from_file, from_list, randint


def test_randint():
    with patch("random.randint") as mock_rand:
        number = randint(min=0, max=100)
        mock_rand.assert_called_with(0, 100)
        number = randint(10, 20)
        mock_rand.assert_called_with(10, 20)


def test_from_list():
    value = from_list([42])
    assert value == 42

    with patch("random.choice") as mock_rand:
        from_list([1, 2, 3, 4])
        mock_rand.assert_called_with([1, 2, 3, 4])


def test_from_file():
    with patch("builtins.open", new_callable=mock_open, read_data="a"):
        assert from_file("test.txt") == "a"

    with patch("builtins.open", new_callable=mock_open, read_data="a\nb\nc\n"):
        with patch("random.choice") as mock_rand:
            from_file("something.txt")
            mock_rand.assert_called_with(["a", "b", "c"])
