from graia.application import GraiaMiraiApplication
from graia.application.event.mirai import *
from graia.application.exceptions import *
from graia.application.message.elements.internal import At
from graia.application.message.elements.internal import MessageChain
from graia.application.message.elements.internal import Plain

import utils
from sagiri_core.core import SagiriGraiaPlatformCore

config = utils.load_config()
platform = SagiriGraiaPlatformCore.get_platform_instance()
loop = platform.get_loop()
bcc = platform.get_bcc()
app: GraiaMiraiApplication = platform.get_app()


@bcc.receiver("MemberJoinEvent")
async def member_join(event: MemberJoinEvent):
    try:
        await app.sendGroupMessage(
            event.member.group.id, MessageChain.create([
                At(target=event.member.id),
                Plain(text="我是本群小可爱纱雾哟~欢迎呐~一起快活鸭~")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("MemberLeaveEventQuit")
async def member_leave(event: MemberLeaveEventQuit):
    try:
        await app.sendGroupMessage(
            event.member.group.id, MessageChain.create([
                Plain(text="%s怎么走了呐~是因为偷袭了69岁的老同志吗嘤嘤嘤" % event.member.name)
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("MemberMuteEvent")
async def member_muted(event: MemberMuteEvent):
    if event.operator is not None:
        if event.member.id == config["HostQQ"]:
            try:
                await app.unmute(event.member.group.id, event.member.id)
                await app.sendGroupMessage(
                    event.member.group.id, MessageChain.create([
                        Plain(text="保护！保护！")
                    ])
                )
            except PermissionError:
                pass
        else:
            try:
                m, s = divmod(event.durationSeconds, 60)
                h, m = divmod(m, 60)
                await app.sendGroupMessage(
                    event.member.group.id, MessageChain.create([
                        Plain(text="哦~看看是谁被关进小黑屋了？\n"),
                        Plain(text="哦我的上帝啊~是%s！他将在小黑屋里呆%s哦~" % (event.member.name, "%02d:%02d:%02d" % (h, m, s)))
                    ])
                )
            except AccountMuted:
                pass


@bcc.receiver("MemberUnmuteEvent")
async def member_unmuted(event: MemberUnmuteEvent):
    try:
        await app.sendGroupMessage(
            event.member.group.id, MessageChain.create([
                Plain(text="啊嘞嘞？%s被放出来了呢~" % event.member.name)
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("MemberLeaveEventKick")
async def member_kicked(event: MemberLeaveEventKick):
    try:
        await app.sendGroupMessage(
            event.member.group.id, MessageChain.create([
                Plain(text="%s滚蛋了呐~" % event.member.name)
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("MemberSpecialTitleChangeEvent")
async def member_special_title_change(event: MemberSpecialTitleChangeEvent):
    try:
        await app.sendGroupMessage(
            event.member.group.id, MessageChain.create([
                Plain(text="啊嘞嘞？%s的群头衔从%s变成%s了呐~" %
                           (event.member.name, event.origin, event.current))
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("MemberPermissionChangeEvent")
async def member_permission_change(event: MemberPermissionChangeEvent):
    try:
        await app.sendGroupMessage(
            event.member.group.id, MessageChain.create([
                Plain(text="啊嘞嘞？%s的权限变成%s了呐~跪舔大佬！" %
                           (event.member.name, event.current))
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("BotLeaveEventKick")
async def bot_leave_group(event: BotLeaveEventKick):
    print("bot has been kicked!")
    await app.sendFriendMessage(
        config["HostQQ"], MessageChain.create([
            Plain(text=f"呜呜呜主人我被踢出{event.group.name}群了")
        ])
    )


@bcc.receiver("GroupNameChangeEvent")
async def group_name_changed(event: GroupNameChangeEvent):
    try:
        await app.sendGroupMessage(
            event.group, MessageChain.create([
                Plain(
                    text=f"群名改变啦！告别过去，迎接未来哟~\n本群名称由{event.origin}变为{event.current}辣！")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("GroupEntranceAnnouncementChangeEvent")
async def group_entrance_announcement_changed(event: GroupEntranceAnnouncementChangeEvent):
    try:
        await app.sendGroupMessage(
            event.group, MessageChain.create([
                Plain(
                    text=f"入群公告改变啦！注意查看呐~\n原公告：{event.origin}\n新公告：{event.current}")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("GroupAllowAnonymousChatEvent")
async def group_allow_anonymous_chat_changed(event: GroupAllowAnonymousChatEvent):
    try:
        await app.sendGroupMessage(
            event.group, MessageChain.create([
                Plain(
                    text=f"匿名功能现在{'开启辣！畅所欲言吧！' if event.current else '关闭辣！光明正大做人吧！'}")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("GroupAllowConfessTalkEvent")
async def group_allow_confess_talk_changed(event: GroupAllowConfessTalkEvent):
    try:
        await app.sendGroupMessage(
            event.group, MessageChain.create([
                Plain(
                    text=f"坦白说功能现在{'开启辣！快来让大家更加了解你吧！' if event.current else '关闭辣！有时候也要给自己留点小秘密哟~'}")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("GroupAllowMemberInviteEvent")
async def group_allow_member_invite_changed(event: GroupAllowMemberInviteEvent):
    try:
        await app.sendGroupMessage(
            event.group, MessageChain.create([
                Plain(
                    text=f"现在{'允许邀请成员加入辣！快把朋友拉进来玩叭！' if event.current else '不允许邀请成员加入辣！要注意哦~'}")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("MemberCardChangeEvent")
async def member_card_changed(event: MemberCardChangeEvent, group: Group):
    try:
        await app.sendGroupMessage(
            group, MessageChain.create([
                Plain(
                    text=f"啊嘞嘞？{event.member.name}的群名片被{event.operator.name}从{event.origin}改为{event.current}了呢！")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("NewFriendRequestEvent")
async def new_friend_request(event: NewFriendRequestEvent):
    await app.sendFriendMessage(
        config["HostQQ"], MessageChain.create([
            Plain(text=f"主人主人，有个人来加我好友啦！\n"),
            Plain(text=f"ID：{event.supplicant}\n"),
            Plain(text=f"来自：{event.nickname}\n"),
            Plain(text=f"描述：{event.message}\n"),
            Plain(text=f"source：{event.sourceGroup}")
        ])
    )


@bcc.receiver("MemberJoinRequestEvent")
async def new_member_join_request(event: MemberJoinRequestEvent):
    try:
        await app.sendGroupMessage(
            event.groupId, MessageChain.create([
                Plain(text=f"有个新的加群加群请求哟~管理员们快去看看叭！\n"),
                Plain(text=f"ID：{event.supplicant}\n"),
                Plain(text=f"昵称：{event.nickname}\n"),
                Plain(text=f"描述：{event.message}\n")
            ])
        )
    except AccountMuted:
        pass


@bcc.receiver("BotInvitedJoinGroupRequestEvent")
async def bot_invited_join_group(event: BotInvitedJoinGroupRequestEvent):
    if event.supplicant != config["HostQQ"]:
        await app.sendFriendMessage(
            config["HostQQ"], MessageChain.create([
                Plain(text=f"主人主人，有个人拉我进群啦！\n"),
                Plain(text=f"ID：{event.supplicant}\n"),
                Plain(text=f"来自：{event.nickname}\n"),
                Plain(text=f"描述：{event.message}\n")
            ])
        )
