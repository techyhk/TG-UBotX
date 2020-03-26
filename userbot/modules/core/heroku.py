# Copyright (C) 2020 Adek Maulana. (github.com/adekmaulana/ProjectBish)
# All rights reserved.
"""
   Heroku manager for your userbot
"""

import heroku3
import asyncio
import os

from asyncio import create_subprocess_shell as asyncSubprocess
from asyncio.subprocess import PIPE as asyncPIPE

from ..help import add_help_item
from userbot import LOGS, HEROKU_APPNAME, HEROKU_APIKEY
from userbot.events import register
from userbot.prettyjson import prettyjson

Heroku = heroku3.from_key(HEROKU_APIKEY)


async def subprocess_run(cmd, heroku):
    subproc = await asyncSubprocess(cmd, stdout=asyncPIPE, stderr=asyncPIPE)
    stdout, stderr = await subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        await heroku.edit(
            '**An error was detected while running subprocess**\n'
            f'```exitCode: {exitCode}\n'
            f'stdout: {stdout.decode().strip()}\n'
            f'stderr: {stderr.decode().strip()}```')
        return exitCode
    return stdout.decode().strip(), stderr.decode().strip(), exitCode


@register(outgoing=True, pattern=r"^\.(set|get|del) var(?: |$)(.*)(?: |$)")
async def variable(var):
    if HEROKU_APPNAME is not None:
        app = Heroku.app(HEROKU_APPNAME)
    else:
        await var.edit("`[HEROKU]:\nPlease setup your` **HEROKU_APPNAME**")
        return
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "get":
        await var.edit("`Getting information...`")
        try:
            val = var.pattern_match.group(2).split()[0]
            await asyncio.sleep(3)
            if val in heroku_var:
                await var.edit("**Config vars**:"
                               f"\n\n`{val} = {heroku_var[val]}`\n")
            else:
                await var.edit("**Config vars**:"
                              f "\n\n`Error -> {val} not exists`")
            return
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await var.edit("`[HEROKU]` variables:\n\n"
                                   "================================"
                                   f"\n```{result}```\n"
                                   "================================"
                                   )
            os.remove("configs.json")
            return
    elif exe == "set":
        await var.edit("`Setting information...`")
        val = var.pattern_match.group(2).split()
        try:
            val[1]
        except IndexError:
            await var.edit("`.set var <config name> <value>`")
            return
        await asyncio.sleep(3)
        if val[0] in heroku_var:
            await var.edit(f"**{val[0]}**  `successfully changed to`  **{val[1]}**")
        else:
            await var.edit(f"**{val[0]}**  `successfully added with value: **{val[1]}**")
        heroku_var[val[0]] = val[1]
        return
    elif exe == "del":
        await var.edit("`Getting information to deleting vars...`")
        try:
            val = var.pattern_match.group(2).split()[0]
        except IndexError:
            await var.edit("`Please specify config vars you want to delete`")
            return
        await asyncio.sleep(3)
        if val in heroku_var:
            await var.edit(f"**{val}**  `successfully deleted`")
            del heroku_var[val]
        else:
            await var.edit(f"**{val}**  `is not exists`")
        return


@register(outgoing=True, pattern=r"^\.heroku(?: |$)")
async def heroku_manager(heroku):
    await heroku.edit("`Processing...`")
    await asyncio.sleep(3)
    result = await subprocess_run(f'heroku ps -a {HEROKU_APPNAME}', heroku)
    if result[2] != 0:
        return
    hours_remaining = result[0]
    await heroku.edit('`' + hours_remaining + '`')
    return


add_help_item(
    "heroku",
    "Core",
    "Manage your heroku vars.",
    """
    `.heroku`
    **Usage:** Check your heroku dyno hours remaining.
    
    `.set var <NEW VAR> <VALUE>`
    **Usage:** add new variable or update existing value variable.
    
    `.get var or .get var <VAR>`
    **Usage:** get your existing varibles, use it only on your private group!
    This returns all of your private information, please be caution...
    
    `.del var <VAR>`
    **Usage:** delete existing variable.
    """
)