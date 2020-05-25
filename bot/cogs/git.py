from discord.ext import commands
import json
import glob
import os


class ManMessage:
    def __init__(self, line_len=72):
        self.name = ''
        self.synopsis = ''
        self.options = {}
        self.short_desc = ''
        self.long_desc = ''
        self.examples = {}
        self.line_len = line_len

    @classmethod
    def load(cls, filename, line_len=72):
        with open(filename, 'r') as f:
            data = json.load(f)
            instance = cls(line_len)
            instance.name = cls.deserialize(data, 'name', '')
            instance.synopsis = cls.deserialize(data, 'synopsis', '')
            instance.options = cls.deserialize(data, 'options', {})
            instance.short_desc = cls.deserialize(data, 'short_desc', '')
            instance.long_desc = cls.deserialize(data, 'long_desc', '')
            instance.examples = cls.deserialize(data, 'examples', {})
            return instance

    @classmethod
    def deserialize(cls, data, name, default):
        if name not in data:
            return default
        return cls.deserialize_field(data[name])

    @classmethod
    def deserialize_field(cls, field):
        if isinstance(field, str):
            return field
        if isinstance(field, list):
            return ''.join(field)
        if isinstance(field, dict):
            return dict(map(lambda x: (x[0], cls.deserialize_field(x[1])), field.items()))
        raise TypeError(
            f'Field of type \'{type(field)}\' is not deserializable')

    def _wrap(self, text, line_len=72, indent=0, indent_first_line=False):
        lines = []
        line_start = 0      # an index into 'text', indicating where the current line starts
        word_start = -1     # -1 means no word is currently being processed
        column = 0          # column on current line

        line_limit = line_len
        if indent_first_line:
            line_limit = line_len - indent

        for i, c in enumerate(text):
            if c.isspace():
                word_start = -1
            elif word_start == -1:
                word_start = i

            if column >= line_limit or c == '\n':
                if word_start == -1:  # if c == '\n', then word_start == -1
                    lines.append(text[line_start:i])
                    line_start = i
                    column = 0

                    # skip one character forward
                    if c == '\n' or c == ' ':
                        line_start += 1
                else:
                    lines.append(text[line_start:word_start])
                    line_start = word_start
                    column = i - word_start

                # all lines after the first will be indented
                line_limit = line_len - indent
            else:
                column += 1

        if line_start < len(text):
            lines.append(text[line_start:len(text)])

        return self._indent(lines, indent, indent_first_line)

    def _indent(self, lines, indent=4, indent_first_line=True):
        prefix = '\n' + ' ' * indent
        result = prefix.join(lines)
        if indent_first_line:
            result = ' ' * indent + result
        return result

    def _short_desc(self):
        return '' if self.short_desc == '' else f'- {self.short_desc}'

    def _synopsis(self):
        indent = 4 + len(self.name) + 1
        return self._wrap(self.synopsis, self.line_len, indent)

    def _options(self):
        if len(self.options) == 0:
            return ''

        lines = []
        for name, value in self.options.items():
            lines.append(name)
            wrapped_lines = self._wrap(
                value, self.line_len - 4, 4, True
            ).split('\n')
            for line in wrapped_lines:
                lines.append(line)
        return self._indent(lines, 4, False)

    def _examples(self):
        if len(self.examples) == 0:
            return ''

        lines = []
        for example in self.examples.values():
            lines.append(example)
            lines.append('')
        return self._wrap('\n'.join(lines), self.line_len, 4)

    def __str__(self):
        return f'''```
                        GIT MANUAL

NAME
    {self.name} {self._short_desc()}

SYNOPSIS
    {self._synopsis()}

DESCRIPTION
    {self._wrap(self.long_desc, self.line_len, 4)}

OPTIONS
    {self._options()}

EXAMPLES
    {self._examples()}
```'''

    __repr__ = __str__


class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._load_commands()

    def _load_commands(self):
        self.messages = {}
        path = 'data/git/git-*.json'
        files = glob.glob(path)
        for f in files:
            name = os.path.basename(f)[:-5]
            self.messages[name] = ManMessage.load(f)

    @commands.group(help='Presents information about various git commands')
    async def git(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
        elif ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command.')
            await ctx.send_help(ctx.command)

    @git.command(help='Create an empty Git repository')
    async def init(self, ctx):
        await ctx.send(self.messages['git-init'])

    @git.command(help='Get or set repository or global configuration')
    async def config(self, ctx):
        await ctx.send(self.messages['git-config'])

    @git.command(help='Pulls commits from a remote to a local branch')
    async def pull(self, ctx):
        await ctx.send(self.messages['git-pull'])

    @git.command(help='Clones a repository into a new directory')
    async def clone(self, ctx):
        await ctx.send(self.messages['git-clone'])


def setup(bot):
    bot.add_cog(Git(bot))
