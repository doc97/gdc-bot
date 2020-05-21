from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import datetime


class Break(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduler= AsyncIOScheduler({'apscheduler.timezone': 'Europe/Helsinki'}) 
        self.scheduler.start()
        self.setup_in_progress = False

    @commands.group(name='break', help='Handles reminders for break time')
    async def _break(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send_help(ctx.command)

    @_break.command(help='Shows the breaks that have been set up')
    async def show(self, ctx):
        jobs = self.scheduler.get_jobs()
        if len(jobs) == 0:
            await ctx.send('No job setup. Schedule on with \'!break setup\'.')
        else:
            jobs_str = [self.job_tostring(j, f'Break #{i}', j.id)
                        for i, j in enumerate(jobs)]
            await ctx.send('\n'.join(jobs_str))

    @_break.command(help='Removes a break by id')
    async def remove(self, ctx, id):
        if self.scheduler.get_job(id) is None:
            await ctx.send(f'No break with id \'{id}\' exists.')
        else:
            self.scheduler.remove_job(id)
            await ctx.send(f'Break with id \'{id}\' removed successfully.')

    @_break.command(help='Removes all breaks.')
    async def clear(self, ctx):
        self.scheduler.remove_all_jobs()
        await ctx.send('All breaks have been removed successfully.')

    @_break.command(help='Sets up the break time interactively, use \'!break abort\' to abort')
    async def setup(self, ctx, id=None):
        if self.setup_in_progress:
            await ctx.send('Another break setup is in progress, please wait for it to finish.')
            return
        self.setup_in_progress = True

        job_id = id if id is not None else f'break_{len(self.scheduler.get_jobs()) + 1}'

        def check_context(m):
            return m.channel == ctx.channel and m.author == ctx.author

        def check_command(m):
            # Only allow '!break abort' through
            return m.content == '!break abort' or not m.content.startswith(ctx.prefix)

        def check_range(m, lower_inc, upper_inc):
            try:
                num = int(m.content)
                return num >= lower_inc and num <= upper_inc
            except ValueError:
                return False

        def check_message(m):
            return check_context(m) and check_command(m)

        def check_weekday(m):
            if not check_context(m):
                return False
            if check_command(m):
                return True
            if m.content in ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']:
                return True
            return check_range(m, 0, 6)

        def check_hour(m):
            if not check_context(m):
                return False
            if check_command(m):
                return True
            return check_range(m, 0, 23)

        def check_minute(m):
            if not check_context(m):
                return False
            if check_command(m):
                return True
            return check_range(m, 0, 59)

        timeout_err_msg = 'Took too long to answer, aborting break time setup.'

        msg = await self._prompt(ctx, 'Message?', check_message, timeout_err_msg, 60.0)
        if msg is None:
            return

        weekday = await self._prompt(ctx, 'Week day?', check_weekday, timeout_err_msg, 60.0)
        if weekday is None:
            return

        hour = await self._prompt(ctx, 'Hour(s)?', check_hour, timeout_err_msg, 60.0)
        if hour is None:
            return

        minute = await self._prompt(ctx, 'Minute(s)?', check_minute, timeout_err_msg, 60.0)
        if minute is None:
            return

        try:
            self.scheduler.add_job(send_message, 'cron', args=[ctx, msg], name=msg,
                                         id=job_id, replace_existing=True,
                                         day_of_week=weekday, hour=hour, minute=minute)
            await ctx.send('Break setup successfully.')
        except ValueError:
            await ctx.send('Invalid argument format(s)! Try again.')

        self.setup_in_progress = False

    async def _prompt(self, ctx, msg, check, err_msg=None, timeout_sec=60.0):
        await ctx.send(msg)
        try:
            reply = await self.bot.wait_for('message', check=check, timeout=timeout_sec)
            if reply.content == '!break abort':
                await self._abort_setup(ctx, 'Setup aborted.')
                return None
            return reply.content
        except asyncio.TimeoutError:
            await self._abort_setup(ctx, err_msg)
            return None

    async def _abort_setup(self, ctx, msg=None):
        if msg is not None:
            await ctx.send(msg)
        self.setup_in_progress = False

    def job_tostring(self, job, title, id):
        t = job.trigger
        fields = {f.name: str(f) for f in t.fields}
        time = datetime.time(hour=int(fields['hour']),
                             minute=int(fields['minute']))
        return f'''{title} (id: {id})
Message: {job.name}
When: every {fields['day_of_week']} at {time}
'''


async def send_message(ctx, msg):
    await ctx.send(msg)


def setup(bot):
    bot.add_cog(Break(bot))
