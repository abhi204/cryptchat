import urwid as uw
import random

lorem_ipsum = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris facilisis rutrum porta. Cras elit urna, viverra ac nisi ornare, faucibus scelerisque tortor. Donec consectetur lacinia felis, ut rutrum turpis pulvinar eu. Nunc mattis mauris euismod, mollis velit vel, iaculis ex. Nulla tincidunt consequat turpis, ut consectetur risus commodo sed. Vestibulum et tellus id velit tempus commodo ut nec metus. Nam et eros erat. Integer mattis risus sem, dapibus tristique lacus elementum a. Nulla sed elit nec lacus varius faucibus vel quis magna. Praesent bibendum orci non varius faucibus. Phasellus eget fermentum ligula, nec eleifend elit. Donec at tortor vel sem euismod blandit vitae sed nunc.
Fusce euismod cursus dolor at tincidunt. In vestibulum auctor pharetra. In ornare porttitor arcu, sit amet sagittis tellus. Phasellus consequat iaculis leo in tincidunt. Nunc a elit vitae nisl vestibulum accumsan ut lobortis augue. Aenean dignissim purus ut ante maximus, id semper tellus sodales. Fusce feugiat mi ligula, euismod suscipit neque rutrum sit amet. Pellentesque elit ipsum, maximus a pulvinar sed, dapibus vel purus. Cras in egestas nisl, nec bibendum diam. Cras nec laoreet metus. Etiam pellentesque nunc convallis, ultricies dolor nec, dignissim turpis. Morbi maximus arcu risus, et cursus quam ultricies et. In euismod quis metus in bibendum. Ut pharetra, dui eget venenatis condimentum, dui sem tincidunt est, in consequat ante diam nec purus. Etiam ut mi a odio mollis mollis.
Etiam vestibulum metus eu fermentum mattis. Ut tincidunt, nisl non euismod ornare, ex nulla convallis mauris, sit amet aliquam ante nulla ut ante. Nullam eleifend vestibulum magna posuere vestibulum. Vivamus mattis eros at suscipit viverra. Nullam arcu libero, blandit a quam et, cursus vehicula sapien. Quisque in porta tellus, sit amet rhoncus enim. In finibus tempus purus ac sodales. Suspendisse potenti. Fusce in velit mollis, placerat tortor tincidunt, rutrum odio. Duis efficitur dui eget sem interdum, id sodales ex facilisis. Praesent tempus auctor tellus, at placerat urna rutrum id.
Phasellus molestie mauris eu accumsan cursus. In tristique purus vel viverra porttitor. Vestibulum sed mi fringilla, cursus ipsum vitae, aliquet mauris. Aliquam a dui neque. Morbi ac libero nec mi lobortis semper quis sit amet tortor. Mauris neque ligula, rutrum sit amet dictum sed, auctor quis arcu. Nulla ipsum libero, feugiat eu turpis quis, condimentum placerat felis. Fusce euismod nulla mauris, vitae faucibus erat lacinia ut. Quisque porta, felis et rhoncus aliquam, magna justo hendrerit nisl, porta hendrerit sem magna quis nulla. Nam vitae est eu orci porttitor volutpat vel ac nisi. Cras sit amet orci quis neque porttitor maximus. Fusce vitae semper felis, vitae condimentum tortor. Maecenas aliquam, enim et ultricies imperdiet, sapien mauris sodales nisl, sed maximus ante massa at augue.
Nam semper, magna ac commodo dictum, turpis mauris cursus libero, a bibendum mauris dui sit amet mauris. Sed at urna vitae lorem consectetur sodales. Cras dui ligula, hendrerit id nunc tempor, vestibulum convallis ipsum. Mauris pretium quis nibh vitae consequat. Ut vestibulum tellus sit amet tellus sodales congue. Etiam porttitor mollis ipsum vitae mollis. Nullam bibendum consectetur lorem. Vivamus et fermentum neque. Duis mattis leo eget purus sollicitudin malesuada. Cras ut tortor tempor, iaculis elit condimentum, ullamcorper augue. Quisque in quam euismod, venenatis diam eget, egestas felis. Curabitur vel risus elit.ArithmeticError
'''

def get_msgs(n):
    from interface import MsgPop
    users = ['you', 'user_x']
    texts = lorem_ipsum.split('\n')
    msg_pops = []
    for i in range(n):
        user = users[random.randint(0,1)]
        text = texts[random.randint(0, len(texts)-2)]
        pop = MsgPop(user, text)
        msg_pops.append(pop)

    return msg_pops

def get_userlist(n):
    group = []
    user_rbs = []
    for i in range(n):
        rb = uw.RadioButton(group,label=f'User {i}')
        user_rbs.append(rb)

    return user_rbs


    