import pytest
import bot.cogs.git as git


class TestManMessage():

    @pytest.mark.parametrize('text, result', [
        ('a'*72, 'a'*72),
        ('a'*72 + ' b', 'a'*72 + '\nb'),
        ('a'*71 + ' b', 'a'*71 + ' \nb'),
    ])
    def test_wrap_no_indent(self, text, result):
        msg = git.ManMessage(name='test', synopsis='test command')
        assert msg._wrap(text, line_len=72) == result

    @pytest.mark.parametrize('text, result, indent', [
        ('a'*72 + ' b', 'a'*72 + '\n   b', 3),
        ('a'*71 + ' b', 'a'*71 + ' \n    b', 4),
    ])
    def test_wrap_indent_wrapped(self, text, result, indent):
        msg = git.ManMessage(name='test', synopsis='test command')
        assert msg._wrap(text=text, line_len=72, indent=indent) == result

    @pytest.mark.parametrize('text, result', [
        ('aaaa', '    aaaa'),
        ('a'*67 + ' b', '    '+'a'*67 + ' \n    b'),
    ])
    def test_wrap_indent_all(self, text, result):
        msg = git.ManMessage(name='test', synopsis='test command')
        assert msg._wrap(text=text, line_len=72, indent=4,
                         indent_first_line=True) == result
