# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

import sys
import io

from random import randint
from time import sleep
from os import execl

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.utils import time_formatter


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        return await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep ([0-9]+)$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    counter = int(time.pattern_match.group(1))
    await time.edit("`I am sulking and snoozing...`")
    if BOTLOG:
        str_counter = time_formatter(counter)
        await time.client.send_message(
            BOTLOG_CHATID,
            f"You put the bot to sleep for {str_counter}.",
        )
    sleep(counter)
    await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern="^.shutdown$")
async def killthebot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Goodbye...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def killdabot(event):
    await event.edit("`*i would be back in a moment*`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot Restarted")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit(
        "Here's something for you to read:\n"
        "\n[TG-UBotX's README.md](https://github.com/HitaloSama/TG-UBotX/blob/master/README.md)"
        "\n[Setup Guide - Basic](https://telegra.ph/How-to-host-a-Telegram-Userbot-11-02)"
        "\n[Setup Guide - Google Drive](https://telegra.ph/How-To-Setup-Google-Drive-04-03)"
        "\n[Setup Guide - LastFM Module](https://telegra.ph/How-to-set-up-LastFM-module-for-Paperplane-userbot-11-02)")


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        "[Repo](https://github.com/HitaloSama/TG-UBotX) GitHub's page."
    )


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`")


add_help_item(
    "misc",
    "Misc",
    "Some misc commands.",
    """
    `.raw`
    **Usage:** Get detailed JSON-like formatted data about replied message.

    `.random` <item1> <item2> ... <itemN>
    **Usage:** Get a random item from the list of items.

    `.repeat` <no.> <text>
    **Usage:** Repeats the text for a number of times. Don't confuse this with spam tho.

    `.restart`
    **Usage:** Restarts the bot!

    `.repo`
    **Usage:** If you are curious what makes the userbot work, this is what you need.

    `.readme`
    **Usage:** Provide links to setup the userbot and it's modules.

    `.shutdown`
    **Usage:** Sometimes you need to shut down your bot. Sometimes you just hope to
    hear Windows XP shutdown sound... but you don't.

    `.sleep` <seconds>
    **Usage:** Userbots get tired too. Let yours snooze for a few seconds.

    `.raw`
    **Usage:** Get detailed JSON-like formatted data about replied message.
    """
)
