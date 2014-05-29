from network import Listener, Handler, poll

handlers = {}  
allNames = {} 
allSubs = {} 

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            allNames[name] = self
            broadcast({'join': name, 'users': handlers.values()})
            print msg
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            publish = [word[1:] for word in txt.split() if word.startswith("#") ]
            subscribers =  [word[1:] for word in txt.split() if word.startswith("+") ]
            unsubscribers =  [word[1:] for word in txt.split() if word.startswith("-") ]
            private =  [word[1:] for word in txt.split() if word.startswith("@") ]
            if len(subscribers) > 0: 
                for s in subscribers:
                    if s in allSubs:
                        allSubs[s].append(self)
                    else:
                        allSubs[s] = [self]
            if len(publish) > 0:
                for p in publish:
                    if p in allSubs:
                        for h in allSubs[p]:
                            h.do_send({'speak': name, 'txt': txt})
            if len(unsubscribers) > 0: 
                for p in unsubscribers:
                    if p in allSubs:
                        allSubs[p].remove(self)
            if len(private) > 0:
               privateName = private[0] 
               sep = '@'
               rest = msg["txt"].split(sep, 1)[0]
               allNames[privateName].do_send({'speak': name, 'txt': rest})
            elif (len(subscribers) ==0) and (len(publish) == 0):
                broadcast({'speak': name, 'txt': txt})



Listener(8888, MyHandler)
while 1:
    poll(0.05)