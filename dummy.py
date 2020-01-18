import this
import random

def get_msgs(n):
    from interface import msg_pop
    users = ['you', 'user_x']
    texts = this.s.split('\n')
    msg_pops = []
    for i in range(n):
        user = users[random.randint(0,1)]
        text = texts[random.randint(0, len(texts)-1)]*10
        pop = msg_pop(user, text)
        msg_pops.append(pop)

    return msg_pops


    