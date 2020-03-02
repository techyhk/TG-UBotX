
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName

from ..help import add_help_item
import userbot.utils.cas_api as cas
from userbot.events import register, errors_handler


async def get_user(event): #kanged get user
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.from_id))
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            self_user = await event.client.get_me()
            user = self_user.id
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                replied_user = await event.client(GetFullUserRequest(user_id))
                return replied_user
        try:
            user_object = await event.client.get_entity(user)
            replied_user = await event.client(GetFullUserRequest(user_object.id))
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return replied_user


@register(pattern="\.cascheck(?: |$)(.*)", outgoing=True)
@errors_handler
async def caschecker(event):
    if not event.text[0].isalpha() and event.text[0] in ("."):
        if event.fwd_from:
            return
    replied_user = await get_user(event)
    if replied_user is None:
        text = "Failed to extract a user from given data"
        await event.edit(text, parse_mode="html")
        return
    user_analysis = replied_user.user
    text = "<b>USER DATA</b>\n\n"
    text += "ID: " + str(user_analysis.id) + "\n"
    if user_analysis.first_name:
        text += "First name: " + str(user_analysis.first_name) + "\n"
    if user_analysis.last_name:
        text += "Last name: " + str(user_analysis.last_name) + "\n"
    if user_analysis.username:
        text += "Username: @" + str(user_analysis.username) + "\n"
    text += "\n<b>CAS DATA</b>\n\n"
    result = cas.banchecker(user_analysis.id)
    text += "Result: " + str(result) + "\n"
    if result:
        parsing = cas.offenses(user_analysis.id)
        if parsing:
            text += "Total of Offenses: "
            text += str(parsing)
            text += "\n"
        parsing = cas.timeadded(user_analysis.id)
        if parsing:
            parseArray=str(parsing).split(", ")
            text += "Day added: "
            text += str(parseArray[1])
            text += "\nTime added: "
            text += str(parseArray[0])
            text += "\n\nAll times are in UTC"
    await event.edit(text, parse_mode="html")
    return


add_help_item(
    "casinterface",
    "Admin",
    "Checks the CAS Status of a specified user",
    """
    `.cascheck <reply/username/user id>`
    """
)
