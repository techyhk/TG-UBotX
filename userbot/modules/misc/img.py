# Adapted from OpenUserBot

import os
import shutil

from ..help import add_help_item
from userbot.events import register
from userbot.google_images_download import googleimagesdownload


@register(outgoing=True, pattern="^\.img (.*)")
async def img_sampler(event):
    """ For .img command, search and return images matching the query. """
    await event.edit("`Processing...`")
    query = event.pattern_match.group(1)
    lim = findall(r"lim=\d+", query)
    try:
        lim = lim[0]
        lim = lim.replace("lim=", "")
        query = query.replace("lim=" + lim[0], "")
    except IndexError:
        lim = 6
    response = googleimagesdownload()

    # creating list of arguments
    arguments = {
        "keywords": query,
        "limit": lim,
        "format": "jpg",
        "no_directory": "no_directory"
    }

    # passing the arguments to the function
    paths = response.download(arguments)
    lst = paths[0][query]
    await event.client.send_file(
        await event.client.get_input_entity(event.chat_id), lst)
    shutil.rmtree(os.path.dirname(os.path.abspath(lst[0])))
    await event.delete()


add_help_item(
    "image",
    "Misc",
    "Search Google Images and return images that "
    "match the query.",
    """
    `.img (query)`
    """
)
