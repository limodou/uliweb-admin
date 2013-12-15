#coding=utf-8
from uliweb import expose, functions

@expose('/admin')
class AdminView(object):
    @expose('')
    def index(self):
        return {}
    
@expose('/admin/models')
class AdminModelsView(object):
    def __init__(self):
        from uliweb import settings
        
        self.m = []
        for k, v in settings.ADMIN_MODELS.items():
            self.m.append(k)
    
    @expose('')
    def index(self):
        model = request.GET.get('model', '')
            
        if model not in self.m:
            model = ''
        
        template_data = {'table':''}
        
        if model:
            view = functions.ListView(model)

            if 'data' in request.values:
                return json(view.json())
            else:
                result = view.run(json_result=True)
                template_data.update({'table':view})
            
        template_data.update({'models':self.m, 'model':model})
        
        return template_data
    
    def add(self):
        from uliweb_admin.semantic.form_help import SemanticLayout
        from uliweb.form.widgets import Button
        from uliweb.core.html import Tag
        
        model = request.GET.get('model', '')
        Model = functions.get_model(model)
        
        def post_created_form(fcls, model):
            fcls.layout_class = SemanticLayout
            fcls.form_buttons = [
                str(Button(value=_('Save'), _class="ui small blue flat submit button", name="submit", type="submit")),
                str(Tag('a', _('Cancel'), _class="ui small reset gray button")),
                ]
        
        template_data = {'model':model}
        
        fields = [k for k, prop in Model._fields_list 
            if not ((hasattr(prop, 'auto_now') and prop.auto_now) or 
                (hasattr(prop, 'auto_now_add') and prop.auto_now_add))
            ]
        
        view = functions.AddView(model, ok_url=url_for(self.__class__.index, model=model),
            fields=fields,
            post_created_form=post_created_form, 
            template_data=template_data)
        return view.run()
    
    def edit(self):
        model = request.GET.get('model', '')
        id = request.GET.get('id')
        if not id:
            error("Can't found object %s of Model %s" % (id, model))
        
        obj = functions.get_object(model, int(id))
        view = functions.EditView(model, obj=obj, ok_url=url_for(self.__class__.index, model=model))
        return view.run()
    
    def delete(self):
        model = request.GET.get('model', '')
        ids = request.POST.getlist('ids')
        
        Model = functions.get_model(model)
        Model.filter(Model.c.id.in_(ids)).remove()
        return json({'success':True, 'message':'删除成功'})
    
    