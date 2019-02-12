from wxpy import *
from os import *
import time

bot = Bot(cache_path=True)

fh = bot.file_helper

#commands and aliases
cmd = ('cmd', 'command')
pycmd = ('py', 'python', 'pycmd', 'pythoncmd', 'pycommand', 'pythoncommand')
ls = ('list', 'ls')
record = ('record', 'rec')

class Record:
    def __init__(self, chat):
        self.chat = chat
        self.records = []
    
    def log(self, chat=fh):
        chat.send("Records at " + self.chat.name)

        for me in self.records:
            msg = me.sender.name + ": "

            if me.type == TEXT: msg += me.text

            elif me.type == MAP: msg += me.location['label']

            elif me.type == CARD: msg += me.card.name

            elif me.type == SHARING: msg += me.url

            else: 
                msg += '[文件]'
            chat.send(msg)
            #避免过多请求
            time.sleep(0.2)

        chat.send("End of records")

    def __repr__(self):
        return "Record<{}>".format(self.chat.name)

records = {fh.name: Record(fh)}

tuling = Tuling(api_key='7d394f8b700f474a9799b5b085ada4de')

@bot.register(fh, except_self=False)
def fh_forward(msg):
    records[fh.name].records.append(msg)
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
        records[fh.name].log(fh)
    
    #command 'py'
    elif pre in pycmd:
        try:
            fh.send(eval(msg.text[len(pre) + 1:]))
        except Exception as e:
            fh.send("Python: " + str(e))

    #auto reply
    else:
        # tuling.do_reply(msg, at_member=False)
        fh.send('Unknown command: {}'.format(pre))

for f in bot.friends():
    records[f.name] = Record(f) 

for g in bot.groups():
    records[g.name] = Record(g)

@bot.register(bot.groups(), except_self=False)
def forward_groups(msg):
    records[msg.chat.name].records.append(msg)

print(records)

embed()