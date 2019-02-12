from wxpy import *
from os import *

bot = Bot(cache_path=True)

fh = bot.file_helper

#commands and aliases
cmd = ('cmd', 'command')
ls = ('list', 'ls')
record = ('record', 'rec')

class Record:
    def __init__(self, chat):
        self.chat = chat
        self.records = []
        @bot.register(chat, except_self=False)
        def forward(msg):
            self.records.append(msg)
    
    def log(self, chat):
        chat.send("Records at " + self.chat.name)

        for me in self.records:
            msg = me.sender.name + ": "

            if me.type == TEXT: msg += me.text

            elif me.type == MAP: msg += me.location['label']

            elif me.type == CARD: msg += me.card.name

            elif me.type == SHARING: msg += me.url

            else: 
                chat.send(msg)
                me.raw.get('Text')(me.file_name)
                chat.send_file(me.file_name)
                remove(me.file_name)
                return
            chat.send(msg)
        
        chat.send("End of records")

records = [Record(fh)]

tuling = Tuling(api_key='7d394f8b700f474a9799b5b085ada4de')

@bot.register(fh, except_self=False)
def fh_forward(msg):

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
        records[0].log(fh)
    
    #auto reply
    else:
        tuling.do_reply(msg, at_member=False)
        # fh.send('Unknown command: {}'.format(pre))

embed()