from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def greet1(ctx):
    await ctx.send("Say hello!")

    def check(m):
        return m.content == "hello" and m.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    await ctx.send(f"Hello {msg.author}!")


# 一度送信したメッセージを消す
@bot.command()
async def greet2(ctx):
    delete_target_msg = await ctx.send("Say hello!")

    def check(m):
        return m.content == "hello" and m.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)
    await delete_target_msg.delete
    await ctx.send(f"Hello {msg.author}!")


bot.run(token)
