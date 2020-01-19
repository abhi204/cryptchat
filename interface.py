import urwid as uw
from dummy import get_msgs, get_userlist

palette = [
        ('sender_client', 'white', 'dark red'),
        ('sender_user', 'white', 'dark blue'),
        ('send_btn', 'black', 'dark green'),
        ('legend', 'black', 'white'),
]

class MsgPop(uw.WidgetWrap):
    def __init__(self, user, msg,):
        super().__init__(self.create_pop(user, msg))

    def create_pop(self, user, msg):
        user_label = uw.Text(user,)
        if user=='you':
            user_label = uw.AttrMap(user_label,'sender_client')
        else:
            user_label = uw.AttrMap(user_label,'sender_user')
        text = uw.Text(msg)
        text = uw.Padding(text, left=1, right=1)
        text = uw.LineBox(
            text,
            tlcorner=u'\u2502',
            blcorner=u'\u2502',
            tline='',
            bline='',
            rline='',
            trcorner='',
            brcorner=''
            )
        div = uw.Divider()
        w_cols = [
            (len(user),user_label),
            text
        ]
        w = uw.Columns(w_cols,dividechars=1)
        w = uw.Padding(w, left=1)
        w = uw.Pile([div, w])
        return w


class Interface(uw.WidgetWrap):
    def __init__(self):
        super().__init__(self.main_window())

    def msg_widget(self):
        msg_w = uw.ListBox(get_msgs(50))
        frame = uw.Frame(body=msg_w)
        msg_wrap = uw.LineBox(frame, title='Messages', title_align='left')
        return msg_wrap

    def user_list_widget(self): # dummy users
        ulist = uw.ListBox(get_userlist(50))
        ulist = uw.LineBox(ulist, title='Users', title_align='left')
        return ulist

    def chat_send_widget(self):
        txtbox_w = uw.Edit(multiline=True)
        txtbox_wrap = uw.Filler(txtbox_w)
        txtbox_wrap = uw.BoxAdapter(txtbox_wrap, height=3)
        txtbox_wrap = uw.Padding(txtbox_wrap, align='center', left=1, right=1)
        txtbox_wrap = uw.LineBox(txtbox_wrap, title='Message', title_align='left')
        send_btn = uw.Button('SEND')
        send_wrap = uw.Padding(send_btn, align='center', left=1, right=1)
        send_wrap = uw.Filler(send_wrap, top=1, bottom=1)
        send_wrap = uw.AttrMap(send_wrap, 'send_btn')
        send_wrap = uw.BoxAdapter(send_wrap, height=3)
        send_wrap = uw.Padding(send_wrap, align='center', left=2, right=2)
        send_wrap = uw.Pile([uw.Divider(), send_wrap])
        w_wrap = uw.Columns([txtbox_wrap,(14,send_wrap)],focus_column=0)
        return w_wrap 

    def main_window(self):
        msg_w = self.msg_widget()
        ulist_w = self.user_list_widget()
        input_and_send_w = self.chat_send_widget()
        legend = uw.Text(u' Add User:^X        Settings:^S        Quit:^Q')
        legend = uw.AttrMap(legend, 'legend')
        w_body = uw.Columns([('weight',4,msg_w), ('weight',1,ulist_w)],focus_column=0,dividechars=1)
        w_footer = uw.Pile([input_and_send_w, uw.Divider(), legend],focus_item=0)
        main_w = uw.Frame(body=w_body, footer=w_footer, focus_part='footer')
        main_w = uw.Padding(main_w, align='center',left=1, right=0)
        return main_w

if __name__ == '__main__':
    app = Interface()
    loop = uw.MainLoop(app,palette=palette)
    loop.screen.set_terminal_properties(colors=256)
    loop.run()

