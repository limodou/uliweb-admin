#coding=utf-8
from uliweb import expose, functions
from uliweb.i18n import ugettext_lazy as _

@expose('/admin')
class AdminView(object):
    def __begin__(self):
        functions.require_login()
        if not request.user.is_superuser:
            error('You have not permisstion to visit the page')

    @expose('')
    def index(self):
        return {}
    
@expose('/admin/models')
class AdminModelsView(object):
    def __begin__(self):
        functions.require_login()
        if not request.user.is_superuser:
            error('You have not permisstion to visit the page')
        
    def __init__(self):
        from uliweb import settings
        
        self.m = []
        for k in settings.ADMIN_MODELS.models:
            self.m.append(k)
    
    @expose('')
    def index(self):
        model = request.GET.get('model', '')
        
        if model not in self.m:
            model = ''
        
        template_data = {'table':''}
        
        if model:
            fields = self._get_fields(model, 'list')
            view = functions.ListView(model, fields=fields)

            if 'data' in request.values:
                return json(view.json())
            else:
                result = view.run(json_result=True)
                template_data.update({'table':view})
            
        template_data.update({'models':self.m, 'model':model})
        
        return template_data
    
    def _get_section(self, modelname, type):
        """
        Get section info from settings
        
        model should be model's name
        type should be 'list', 'add', 'edit'
        """
        from uliweb import settings
        
        return settings.get_var('ADMIN_MODEL_%s_%s' % (modelname, type.upper()), {})

    def _get_fields(self, modelname, type):
        """
        Get fields according Model and type
        type should be 'list', 'add', 'edit'
        
        It'll find settings just like 'ADMIN_MODEL_<modelname>_<type>',
        if not found, it'll use Model._fields_list
            
        """
        section = self._get_section(modelname, type)
        fields = section.get('fields')
        
        if not fields:
            fields = [k for k, prop in functions.get_model(modelname)._fields_list 
                if not ((hasattr(prop, 'auto_now') and prop.auto_now) or 
                    (hasattr(prop, 'auto_now_add') and prop.auto_now_add))
                ]
        return fields
        
    def _get_parameters(self, modelname, type, params):
        from uliweb.utils.common import import_attr
        
        d = {}
        section = self._get_section(modelname, type)
        for k, _t in params.items():
            _type = _t.get('type')
            _default = _t.get('default')
            
            v = section.get(k)
            if not v:
                v = _default
            
            if v:
                if _type == 'function':
                    if isinstance(v, (str, unicode)):
                        v = import_attr(v)
                else:
                    if callable(v):
                        v = v()
                d[k] = v
        return d
                    
    def _post_created_form(self, fcls):
        from uliweb.form import SelectField
        from uliweb_admin.semantic.form_help import SemanticLayout
        from uliweb.form.widgets import Button
        from uliweb.core.html import Tag

        fcls.layout_class = SemanticLayout
        fcls.form_buttons = [
            str(Button(value=_('Save'), _class="ui small blue flat submit button", 
                name="submit", type="submit")),
            str(Tag('a', _('Cancel'), _class="ui small reset gray button", 
                href="javascript:history.go(-1);")),
            ]
        #SelectField set empty = False
        for k, v in fcls.fields.items():
            if isinstance(v, SelectField):
                v.empty = None
        
    def add(self):
        
        model = request.GET.get('model', '')
        
        def post_created_form(fcls, model):
            self._post_created_form(fcls)
        
        template_data = {'model':model}
        
        mapping = {
            'pre_save':{'type':'function'},
        }
        
        params = self._get_parameters(model, 'add', mapping)
        
        view = functions.AddView(model, 
            ok_url=url_for(self.__class__.index, model=model),
            fields=self._get_fields(model, 'add'),
            post_created_form=post_created_form, 
            template_data=template_data,
            **params)
        return view.run()
    
    def edit(self):

        model = request.GET.get('model', '')
        
        id = request.GET.get('id')
        if not id:
            error("There is no id parameter")
        obj = functions.get_object(model, int(id))
        if not obj:
            error("Can't found object %s of Model %s" % (id, model))
        
        def post_created_form(fcls, model, obj):
            self._post_created_form(fcls)
        
        template_data = {'model':model}
        
        mapping = {
            'pre_save':{'type':'function'},
        }
        
        params = self._get_parameters(model, 'edit', mapping)
        
        view = functions.EditView(model, obj=obj, 
            ok_url=url_for(self.__class__.index, model=model),
            fields=self._get_fields(model, 'edit'),
            post_created_form=post_created_form, 
            template_data=template_data,
            **params)
        return view.run()
    
    def delete(self):
        model = request.GET.get('model', '')
        ids = request.POST.getlist('ids')
        
        Model = functions.get_model(model)
        Model.filter(Model.c.id.in_(ids)).remove()
        return json({'success':True, 'message':'删除成功'})
    
    