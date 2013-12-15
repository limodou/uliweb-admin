#coding=utf-8
from uliweb import expose, functions

@expose('/blog')
class BlogView(object):
    def __init__(self):
        self.M = functions.get_model('blog')
        self.C = functions.get_model('blogcategory')
        
    @expose('')
    def index(self):
        page = int(request.GET.get('page', 1) or 1)
        size = 10
        offset = (page - 1)*size
        
        blogs = self.M.all().order_by(self.M.c.created_time.desc()).offset(offset).limit(size)
        categories = self.C.all()
        
        return {'blogs':blogs, 'categories':categories}