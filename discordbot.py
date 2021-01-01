from discord.ext import commands
import discord
import os
import traceback
import textwrap

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
async def boshu(ctx):
    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    announce_msg_title = await ctx.send("募集タイトルを入力してください")
    input_msg_title = await bot.wait_for("message", check=check)
    await discord.Message.delete(announce_msg_title)
    announce_msg_num = await ctx.send("最大募集人数を入力してください")
    input_msg_num = await bot.wait_for("message", check=check)
    await discord.Message.delete(announce_msg_num)
    announce_msg_time = await ctx.send("日付, 時間を入力してください")
    input_msg_time = await bot.wait_for("message", check=check)
    await discord.Message.delete(announce_msg_time)
    announce_msg_misc = await ctx.send("備考, 参加条件などを入力してください")
    input_msg_misc = await bot.wait_for("message", check=check)
    await discord.Message.delete(announce_msg_misc)

    boshu_body = textwrap.dedent(f"""
        @here {input_msg_title.content}募集 ＠{input_msg_num.content}
        ```
        ■募集者: {ctx.author.name}
        ■日付, 時間: {input_msg_time.content}
        ■備考, 参加条件など: {input_msg_misc.content}
        ```""")

    await discord.Message.delete(input_msg_title)
    await discord.Message.delete(input_msg_num)
    await discord.Message.delete(input_msg_time)
    await discord.Message.delete(input_msg_misc)
    await ctx.send(boshu_body)


bot.run(token)
