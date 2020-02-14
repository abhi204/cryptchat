import urwid as uw
from dummy import get_msgs, get_userlist

palette = [
        ('sender_client', 'white', 'dark red'),
        ('sender_user', 'white', 'dark blue'),
        ('send_btn', 'black', 'dark green'),
        ('legend', 'black', 'white'),
        ('dialog', 'black', 'light gray'),
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


class Dialog(uw.WidgetWrap):

    def __init__(self, main_w, height, legend=None, key_handlers=dict()):
        '''
         main_w => Flow widget ( Passed as arg to functions of key_handlers)
         height => height of main_w
         key_handler => dictionary with legend keys mapped to their handler function
        '''
        self.key_handlers = key_handlers
        self.base_w = main_w
        super().__init__(self._create_dialog(main_w, height, legend))
    
    def _create_dialog(self, main_w, height, legend=None):
        div = uw.Divider()
        if legend:
            body = uw.Pile([div, main_w, div], focus_item=1)
            body = uw.BoxAdapter(uw.Filler(body), height+2)
            footer = uw.LineBox(
                legend,
                blcorner='',bline='',brcorner='',
                tlcorner='\u2500', trcorner='\u2500',
                lline='', rline=''
                )
            dialog = uw.Pile([body, footer], focus_item=0)
        else:
            dialog = body
        
        dialog = uw.LineBox(uw.Padding(dialog,left=1, right=1))

        dialog = uw.Filler(
            uw.Padding(dialog,'center', left=1, right=1),
            top=1,
            bottom=1
        )
        dialog = uw.AttrMap(dialog, 'dialog')
        return dialog

    def keypress(self, size, key):
        if key in self.key_handlers:
            handler = self.key_handlers[key]
            handler(self.base_w)
        else:
            super().keypress(size, key)


class Interface(object):
    user_group = []

    def __init__(self):
        self._main_window = self.main_window()
        self.loop = uw.MainLoop(
            self._main_window,
            palette,
            unhandled_input=self.unhandled_input
        )
        self.loop.screen.set_terminal_properties(colors=256)

    def msg_widget(self):
        msg_w = uw.ListBox(get_msgs(50)) # 50 dummy messages
        msg_wrap = uw.LineBox(msg_w, title='Messages', title_align='left')
        msg_w.focus_position = len(msg_w.body) - 1 
        return msg_wrap

    def msg_pop_append(self, sender, msg):
        msg_pop = MsgPop(sender, msg)
        msg_w = self.msg_w.base_widget
        msg_w.body.append(msg_pop)
        msg_w.focus_position = len(msg_w.body)-1

    def user_list_widget(self):
        ulist_walker = uw.SimpleFocusListWalker(get_userlist(50, self.user_group))
        ulist = uw.ListBox(ulist_walker) # 50 dummy users
        ulist = uw.LineBox(ulist, title='Users', title_align='left')
        return ulist

    def chat_send_widget(self):
        txtbox_w = uw.Edit(multiline=True)
        txtbox_wrap = uw.Filler(txtbox_w)
        txtbox_wrap = uw.BoxAdapter(txtbox_wrap, height=3)
        txtbox_wrap = uw.Padding(txtbox_wrap, align='center', left=1, right=1)
        txtbox_wrap = uw.LineBox(txtbox_wrap, title='Message', title_align='left')
        send_btn = uw.Button('SEND', on_press=self.on_send)
        send_wrap = uw.Padding(send_btn, align='center', left=1, right=1)
        send_wrap = uw.Filler(send_wrap, top=1, bottom=1)
        send_wrap = uw.AttrMap(send_wrap, 'send_btn')
        send_wrap = uw.BoxAdapter(send_wrap, height=3)
        send_wrap = uw.Padding(send_wrap, align='center', left=2, right=2)
        send_wrap = uw.Pile([uw.Divider(), send_wrap])
        w_wrap = uw.Columns([txtbox_wrap,(14,send_wrap)],focus_column=0)
        return w_wrap 

    def on_send(self, *args, **kwargs):
        msg_textbox = self.msg_textbox.base_widget
        msg = msg_textbox.edit_text.rstrip()
        if len(msg):
            # Code for sending message via socket
            self.msg_pop_append('you', msg)
            msg_textbox.set_edit_text('')

    def user_add_window(self):

        # User Add dialog
        txt_box = uw.Edit(caption='Add user: ', multiline=False)
        legend = uw.Columns([
                uw.Text('Continue: [Enter]'),
                uw.Text('Cancel: [Esc]', align='right')
            ])
        dialog = Dialog(
            txt_box,
            1,
            legend,
            {
                'enter': self.user_add,
                'esc': self.close_dialog                
            }
        )

        # Overlay for the new main_loop widget
        w = uw.Overlay(
            dialog,
            self._main_window,
            'center',
            ('relative', 20),
            'middle',
            ('relative', 15),
            min_height=7,
            min_width=40
        )
        return w

    def user_add(self, dialog_w):
        ulist_w = self.ulist_w.base_widget
        username = dialog_w.base_widget.edit_text
        if username:
            user_rb = uw.RadioButton(
                self.user_group,
                dialog_w.base_widget.edit_text
            )
            user_rb.set_state(True)
            ulist_w.body.insert(0, user_rb)
            ulist_w.focus_position = 0
            self.close_dialog()

    def close_dialog(self, *args, **kwargs):
        self.loop.widget = self._main_window

    def main_window(self):
        self.msg_w = self.msg_widget()
        self.ulist_w = self.user_list_widget()
        input_and_send_w = self.chat_send_widget()
        self.msg_textbox, options = input_and_send_w.contents[0]
        legend = uw.Text(u' Add User:^X        Settings:^S        Exit:^E')
        legend = uw.AttrMap(legend, 'legend')
        w_body = uw.Columns([('weight',4,self.msg_w), ('weight',1,self.ulist_w)],focus_column=0,dividechars=1)
        w_footer = uw.Pile([input_and_send_w, uw.Divider(), legend],focus_item=0)
        main_w = uw.Frame(body=w_body, footer=w_footer, focus_part='footer')
        main_w = uw.Padding(main_w, align='center',left=1, right=0)
        return main_w

    def unhandled_input(self, key):
        current_w = self.loop.widget
        if key == 'ctrl x' and current_w == self._main_window :
            self.loop.widget = self.user_add_window()
            return
        if key == 'esc' and current_w != self._main_window :
            self.loop.widget = self._main_window
            return
        if key == 'ctrl e':
            raise uw.ExitMainLoop()

    def run(self):
        self.loop.run()


if __name__ == '__main__':
    Interface().run()

