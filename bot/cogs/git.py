from discord.ext import commands


class ManMessage:
    def __init__(self, name, synopsis, options=[], short_desc='', long_desc=[], examples=[]):
        self.name = name
        self.synopsis = synopsis
        self.options = options
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.examples = examples

    def _wrap(self, text, line_len=72, indent=0, indent_first_line=False):
        lines = []
        line_start = 0      # an index into 'text', indicating where the current line starts
        word_start = -1     # -1 means no word is currently being processed
        column = 0          # column on current line

        line_limit = line_len
        if indent_first_line:
            line_limit = line_len - indent

        for i, c in enumerate(text):
            if word_start == -1 and c.isalpha():
                word_start = i
            if not c.isalpha():
                word_start = -1

            if column >= line_limit or c == '\n':
                if word_start == -1:  # if c == '\n', then word_start == -1
                    lines.append(text[line_start:i])
                    line_start = i
                    column = 0
                    if c == '\n':
                        line_start = i+1
                else:
                    lines.append(text[line_start:word_start])
                    line_start = word_start
                    column = i - word_start

                # all lines after the first will be indented
                line_limit = line_len - indent
            else:
                column += 1
        if column > 0:
            lines.append(text[line_start:len(text)])

        if indent_first_line:
            lines[0] = ' ' * indent + lines[0]
        prefix = '\n' + ' ' * indent
        return prefix.join(lines)

    def _short_desc(self):
        return '' if self.short_desc == '' else f'- {self.short_desc}'

    def _synopsis(self):
        indent = 4 + len(self.name) + 1
        return self._wrap(self.synopsis, 80, indent)

    def _options(self):
        if len(self.options) == 0:
            return ''

        lines = []
        for opt in self.options:
            lines.append(opt[0])
            lines.append(self._wrap(opt[1], 80, 4, True))
        return self._wrap('\n'.join(lines), 80, 4)

    def _examples(self):
        if len(self.examples) == 0:
            return ''

        lines = []
        for i, example in enumerate(self.examples):
            lines.append(f'{i+1}. {example}')
            lines.append('')
        return self._wrap('\n'.join(lines), 80, 4)

    def __str__(self):
        return f'''```
                        GIT MANUAL

NAME
    {self.name} {self._short_desc()}

SYNOPSIS
    {self._synopsis()}

DESCRIPTION
    {self._wrap(self.long_desc, 80-4, 4)}

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
            await ctx.send('Please specify a sub-command, see a list of them with `!help git`.')
        elif ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command.')

    @git.command(help='Prints info on the git init command')
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
    
    @git.command(help='Prints info on the git pull command')
    async def pull(self, ctx):
        msg = ManMessage(
            name='git-pull',
            synopsis='git pull [options] [<repository> [<refspec>...]]',
            options=[
                ('-q, --quiet', 'Only print error and warning messages.'),
                ('-r, --rebase', ('rebases local branch so that conflicts can be avoided that were caused'
                '\n' 
                'by changes in the remote branch.')),
                ('<repository>' , 'should be the name of a remote repository.'),
                ('<refspec>', ('can name an arbitrary remote ref (for example, the name of a tag) '
                '\n' 
                'or even a collection of refs with corresponding remote-tracking branches.'))
            ],
            short_desc='pulls commits from remote to local branch.',
            long_desc=(
                'pulls changes/commits from remote to local branch.\n' 
                '\'git pull\' is a combination of \'git fetch\' and \'git merge\'.'
            )
        )
        await ctx.send(msg)
                

    @git.command(help='Prints info on the git clone command')
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
