import urwid as uw

class interface(uw.WidgetWrap):
    def __init__(self):
        super().__init__(self.main_window())

    def msg_widget(self):
        msg_w = uw.Edit(multiline=True)
        msg_w = uw.Filler(msg_w)
        frame = uw.Frame(body=msg_w)
        msg_wrap = uw.LineBox(frame, title='Messages', title_align='left')
        return msg_wrap

    def user_list_widget(self): # dummy users
        group=[]
        user_rb = []
        for i in range(100):
            rb = uw.RadioButton(group,label=f'User {i}')
            user_rb.append(rb)
        ulist = uw.ListBox(user_rb)
        ulist = uw.LineBox(ulist, title='Users', title_align='left')
        return ulist

    def chat_send_widget(self):
        txtbox_w = uw.Edit(multiline=True)
        txtbox_wrap = uw.Filler(txtbox_w)
        txtbox_wrap = uw.BoxAdapter(txtbox_wrap, height=3)
        txtbox_wrap = uw.LineBox(txtbox_wrap, title='Message', title_align='left')
        send_btn = uw.Button('SEND')
        send_wrap = uw.Filler(send_btn, top=1)
        send_wrap = uw.BoxAdapter(send_wrap, height=5)
        w_wrap = uw.Columns([txtbox_wrap,(10,send_wrap)],focus_column=0)
        return w_wrap 

    def main_window(self):
        msg_w = self.msg_widget()
        ulist_w = self.user_list_widget()
        input_and_send_w = self.chat_send_widget()
        legend = uw.Text(u'Switch User:^X        Settings:^S        Quit:^Q')
        w_body = uw.Columns([('weight',4,msg_w), ('weight',1,ulist_w)],focus_column=0,dividechars=1)
        w_footer = uw.Pile([input_and_send_w, uw.Divider(), legend],focus_item=0)
        main_w = uw.Frame(body=w_body, footer=w_footer, focus_part='footer')
        return main_w

if __name__ == '__main__':
    app = interface()
    loop = uw.MainLoop(app)
    loop.run()

