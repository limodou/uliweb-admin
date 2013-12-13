def call(app, var, env, pagination=True, treegrid=True):
    a = []
    a.append('mmgrid/mmGrid.css')
    a.append('mmgrid/mmGrid.js')
    if treegrid:
        a.append('mmgrid/mmTreeGrid.css')
        a.append('mmgrid/mmTreeGrid.js')
    
    if pagination:
        a.append('mmgrid/mmPaginator.css')
        a.append('mmgrid/mmPaginator.js')
        a.append('mmgrid/scrolling.js')
    return {'toplinks':a, 'depends':['jquery', 'json2']}
