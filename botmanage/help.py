from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
=====================
- HoshinoBot使用说明 -
=====================
[pcr查询]：
1.[pcr速查] 常用网址/图书馆
2.[bcr速查] B服萌新攻略
3.[日rank] rank推荐表
4.[台rank] rank推荐表
5.[陆rank] rank推荐表
6.[挖矿15001] 矿场余钻
7.[黄骑充电表] 黄骑1动规律
8.[谁是霸瞳] 角色别称查询

[pcr娱乐]：
1.[凯露酱来发十连] 转蛋模拟
2.[凯露酱来发单抽] 转蛋模拟
3.[凯露酱来一井] 4w5钻！
4.[查看卡池] 模拟卡池&出率
5.[切换卡池] 更换模拟卡池
6.[切噜一下] 转换为切噜语
7.[切噜～♪切啰巴切拉切蹦切蹦] 切噜语翻译
'''.strip()

def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)


@sv.on_prefix(('help', '帮助', '幫助'))
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        await bot.send(ev, TOP_MANUAL)
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
        await bot.send(ev, msg)
    # else: ignore
