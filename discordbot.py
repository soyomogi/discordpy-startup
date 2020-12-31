from discord.ext import commands
import discord
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
    await discord.Message.delete(delete_target_msg)
    await ctx.send(f"Hello {msg.author}!")


@bot.command()
async def boshu(ctx):
    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    announce_msg1 = await ctx.send("タイトル")
    input_msg1 = await bot.wait_for("message", check=check)
    await discord.Message.delete(announce_msg1)
    announce_msg2 = await ctx.send("時間帯")
    input_msg2 = await bot.wait_for("message", check=check)
    await discord.Message.delete(announce_msg2)

    await ctx.send(f"タイトル: {input_msg1.content}\n時間帯: {input_msg2.content}")


bot.run(token)
