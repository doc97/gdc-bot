from discord.ext import commands


class ManMessage:
    def __init__(self, name, synopsis, options=[], short_desc='', long_desc=[], examples=[], line_len=72):
        self.name = name
        self.synopsis = synopsis
        self.options = options
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.examples = examples
        self.line_len = line_len

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
        for opt in self.options:
            lines.append(opt[0])
            wrapped_lines = self._wrap(
                opt[1], self.line_len - 4, 4, True).split('\n')
            for line in wrapped_lines:
                lines.append(line)
        return self._indent(lines, 4, False)

    def _examples(self):
        if len(self.examples) == 0:
            return ''

        lines = []
        for i, example in enumerate(self.examples):
            lines.append(f'{i+1}. {example}')
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

    @commands.group(help='Presents information about various git commands')
    async def git(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)
        elif ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command.')
            await ctx.send_help(ctx.command)

    @git.command(help='Create an empty Git repository')
    async def init(self, ctx):
        msg = ManMessage(
            name='git-init',
            synopsis='git init [-q | --quiet] [<directory>]',
            options=[
                ('-q, --quiet', 'Only print error and warning messages.'),
                ('<directory>', ('If provided, the command is run inside it. If this directory '
                                 'does not exist it will be created.'))
            ],
            short_desc='Create an empty Git repository',
            long_desc=(
                'This command creates an empty Git repository - basically a .git directory with '
                'subdirectories for objects, refs/heads, refs/tags, and template files.\n'
                '\n'
                'Running \'git init\' in an existing repository is safe. It will not overwrite '
                'things that are already there.'
            )
        )
        await ctx.send(msg)

    @git.command(help='Get or set repository or global configuration')
    async def config(self, ctx):
        msg = ManMessage(
            name='git-config',
            synopsis='git config [<options>] <name> [<value>]',
            options=[
                ('--global', ('For writing options: write to the global `~/.gitconfig` file rather '
                              'than to the repository `.git/config` file.\n'
                              '\n'
                              'For reading options: read from global the `~/.gitconfig` file rather '
                              'than from the repository `.git/config` file.')),
                ('--local', ('This is the default behaviour.\n'
                             '\n'
                             'For writing options: write to the repository `.git/config` file rather '
                             'than to the global `~/.gitconfig` file.\n'
                             '\n'
                             'For reading options: read from the repository `~/.gitconfig` file rather '
                             'than from the global `.git/config` file.')),
                ('-l, --list', 'List all variables and their values in the config file.'),
                ('<name>', 'The name of the configuration variable, e.g. \'user.name\'.'),
                ('<value>', 'Specifying this value sets the configuration variable to this value.')
            ],
            short_desc='Get or set repository or global configuration',
            long_desc=('You can query or set configuration options with this command. You will need to '
                       'at least set up \'user.name\' and \'user.email\'. Note how the variable '
                       'consists of a category and a name in the form of <category>.<name>. All '
                       'variables follow this scheme.'),
            examples=[('Configure global name and email:\n'
                       'git config --global user.name "John Smith"\n'
                       'git config --global user.email "john.smith@example.com"'),
                      ('List repository specific text editor:\n'
                       'git config core.editor'),
                      ('List all configuration variables:\n'
                       'git config -l')]
        )
        await ctx.send(msg)

    @git.command(help='Pulls commits from a remote to a local branch')
    async def pull(self, ctx):
        msg = ManMessage(
            name='git-pull',
            synopsis='git pull [<options>] [<repository> [<refspec>...]]',
            options=[
                ('-q, --quiet', 'Only print error and warning messages.'),
                ('-r, --rebase', ('Rebase instead of merge the remote branch into the local branch '
                                  'so that conflicts can be avoided that were caused by changes in '
                                  'the remote branch leading to a merge commit.')),
                ('<repository>', ('Should be the name of a remote repository. The default value is '
                                  '\'origin\'.')),
                ('<refspec>', ('Can name an arbitrary remote ref (the name of a tag or a branch) '
                               'or even a collection of refs with corresponding remote-tracking '
                               'branches. The default value is the name of the current local branch.'))
            ],
            short_desc='Pulls commits from remote to local branch',
            long_desc=(
                'Pulls changes/commits from a remote and incorporates them into the local branch. '
                '\'git pull\' performs a \'git fetch\' and then a \'git merge\'. If --rebase is used, '
                'it performs a \'git rebase\' instead of the default \'git merge\'.'
            ),
            examples=['Pull with rebase:\ngit pull --rebase',
                      'Pull branch \'dev\' from a remote called \'gitserver\':\ngit pull gitserver dev']
        )
        await ctx.send(msg)

    @git.command(help='Clones a repository into a new directory')
    async def clone(self, ctx):
        msg = ManMessage(
            name='git-clone',
            synopsis='git clone [-q | quiet] [-v | --verbose] <repository> [<directory>]',
            options=[
                ('-q, --quiet', 'Only print error and warning messages.'),
                ('-v, --verbose', 'Print more information.'),
                ('<repository>', ('The (remote) repository to clone from. Usually in the form of a url for '
                                  'example \'https://github.com/<user>/<repo>\'.')),
                ('<directory>', ('The name of a new directory to clone into. By default it is the remote '
                                 'repository name.'))
            ],
            short_desc='Clones a repository into a new directory',
            long_desc=('Clones a repository into a newly created directory. Tracking of remote branches '
                       'are set up and the command also checks out an initial branch, often the master '
                       'branch (see \'git checkout\').\n'
                       '\n'
                       'After the clone, a plain \'git fetch\' is performed to update all tracked branches '
                       'after which a plain \'git pull\' will merge the remote master branch into the '
                       'local master branch.'),
            examples=['Clone with HTTPS:\ngit clone https://github.com/doc97/gdc-bot',
                      'Clone with SSH:\ngit clone git@github.com:doc97/gdc-bot']
        )
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Git(bot))
