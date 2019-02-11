from wxpy import *
from os import *

bot = Bot(cache_path=True)

fh = bot.file_helper

#commands and aliases
cmd = ('cmd', 'command')
ls = ('list', 'ls')
record = ('record', 'rec')

records = [[]]

tuling = Tuling(api_key='7d394f8b700f474a9799b5b085ada4de')

@bot.register(fh, except_self=False)
def fh_forward(msg):
    records[0].append(msg)

    #其他消息类型处理
    if msg.type != TEXT:
        # tuling.do_reply(msg, at_member=False)
        fh.send('Unknown command')
        return

    #文本类型处理
    pre = msg.text.split(' ')[0].lower()
    #command 'cmd'
    if pre in cmd:
        p = popen(msg.text[len(pre) + 1:])
        fh.send(p.read())
    
    #command 'list'
    elif pre in ls:
        param = msg.text[len(pre) + 1:].lower()
        if param == 'friend':
            fh.send(bot.friends())
        elif param == 'group':
            fh.send(bot.groups())
        else:
            fh.send('list: unknown type: {}'.format(param))

    #command 'record'
    elif pre in record:
        for me in records[0]:
            if me.type == TEXT: fh.send(me.text)

            elif me.type == MAP: fh.send(me.location['label'])

            elif me.type == CARD: fh.send(me.card.name)

            elif me.type == SHARING: fh.send(me.url)

            else: 
                me.raw.get('Text')(me.file_name)
                fh.send_file(me.file_name)
                remove(me.file_name)
    
    #auto reply
    else:
        # tuling.do_reply(msg, at_member=False)
        fh.send('Unknown command: {}'.format(pre))

embed()