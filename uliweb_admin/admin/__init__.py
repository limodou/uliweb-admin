from plugs.menus import iter_menu

def menu_render(name, active='', validators=None, id=None, _class=None):
    """
    :param menu: menu item name
    :param active: something like "x/y/z"
    :param check: validate callback, basic validate is defined in settings
    """
    s = []
    for _t, y in iter_menu(name, active, validators):
        index = y['index']
        indent = ' '*index*2
        if _t == 'item':
            if index > 1:
                _cls = ''
                if y['active']:
                    _cls = _cls + 'active '
                s.append('<a class="%sitem" href="%s">%s</a>\n' % (_cls, y['link'], y['title']))
            else:
                #first level
                icon = y.get('icon') or ''
                content = """<div class="header item">
  <i class="%(icon)s icon"></i>
  %(title)s
</div>
"""
                s.append(content % {'icon':icon, 'title':y['title']})
        elif _t == 'open':
            pass
        elif _t == 'close':
            pass
        elif _t == 'begin':
            if index == 0:
                s.append('<div class="ui vertical fluid menu">\n')
            else:
                pass
        else:
            if index == 0:
                s.append('</div>\n')
    
    return ''.join(s)
    
