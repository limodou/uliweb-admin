from uliweb.form.layout import Layout
from uliweb.core.html import Buf, Tag, Div
    
class SemanticLayout(Layout):
    form_class = 'ui form segment'
    field_classes = {
        ('Text', 'Password', 'TextArea'):'input-xlarge',
        ('Button', 'Submit', 'Reset', 'Checkbox', 'File', 'Hidden'):'',
        ('Select', 'RadioSelect'):'',
        ('Radio',):'radio',
        }
    
    def line(self, obj, label, input, help_string='', error=None):
        
        _class = "field"
        if error:
            _class = _class + ' error'
        
        div_group = Div(_class=_class, id='div_'+obj.id, newline=True)
        with div_group: 
            div_group << input.get_label()
#            div = Div(_class='controls', newline=True)
#            with div:
            div_group << input
            if help_string:
                div_group << Tag('p', _class="help help-block", _value=help_string)
            if error:
                div_group << Div(_class="ui red pointing above ui label", _value=error, newline=True)
                    
        return str(div_group)
    
    def _buttons_line(self, buttons):
#        div = Div(_class="form-actions")
        div = Div()
        with div:
            div << buttons
        return div
    
    def body(self):
        buf = Buf()
        if not self.layout:
            self.layout = [name for name, obj in self.form.fields_list]
        self.process_layout(buf)
        return str(buf)

    def process_layout(self, buf):
        if self.form.form_title:
            buf << '<fieldset><legend>%s</legend>' % self.form.form_title
        for line in self.layout:
            if isinstance(line, (tuple, list)):
                with buf.Div(_class='line'):
                    for x in line:
                        f = getattr(self.form, x)
                        obj = self.form.fields[x]
                        if self.is_hidden(obj):
                            #buf << f
                            pass
                        else:
                            buf << self.line(obj, f.label, f, f.help_string, f.error)
            else:
                f = getattr(self.form, line)
                obj = self.form.fields[line]
                if self.is_hidden(obj):
                    #buf << f
                    pass
                else:
                    buf << self.line(obj, f.label, f, f.help_string, f.error)
        if self.form.form_title:
            buf << '</fieldset>'
