from telethon.tl.functions.channels import (
    CreateChannelRequest,
    UpdateUsernameRequest,
    ExportChatInviteRequest,
)
from telethon.tl.functions.messages import CreateChatRequest
from bullove import bullove, client


@bullove(pattern=r"^buat (b|g|c)(?: |$)(.*)")
async def _(e):
    type_of_group = e.pattern_match.group(1).strip()
    group_name = e.pattern_match.group(2)
    username = None

    if " ; " in group_name:
        group_ = group_name.split(" ; ", maxsplit=1)
        group_name = group_[0]
        username = group_[1]

    xx = await e.respond("⏳ Membuat...")

    if type_of_group == "b":
        try:
            r = await e.client(
                CreateChatRequest(users=[e.sender_id], title=group_name)
            )
            created_chat_id = r.chats[0].id
            result = await e.client(ExportChatInviteRequest(peer=created_chat_id))
            await xx.edit(f"✅ Grup **{group_name}** berhasil dibuat!\nLink: {result.link}")
        except Exception as ex:
            await xx.edit(f"❌ Error: {str(ex)}")

    elif type_of_group in ["g", "c"]:
        try:
            r = await e.client(
                CreateChannelRequest(
                    title=group_name,
                    about="Dibuat dengan Bullove Bot",
                    megagroup=type_of_group != "c",
                )
            )
            created_chat_id = r.chats[0].id
            if username:
                await e.client(UpdateUsernameRequest(created_chat_id, username))
                result = f"https://t.me/{username}"
            else:
                result = (
                    await e.client(ExportChatInviteRequest(peer=created_chat_id))
                ).link

            await xx.edit(f"✅ {group_name} berhasil dibuat!\nLink: {result}")
        except Exception as ex:
            await xx.edit(f"❌ Error: {str(ex)}")
