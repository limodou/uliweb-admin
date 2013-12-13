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
        model = request.GET.get('model', '')

        view = functions.AddView(model, ok_url=url_for(self.__class__.index, model=model))
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
    
    