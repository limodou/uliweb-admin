def call(app, var, env):
    a = []
    a.append('mmgrid/mmGrid.css')
    a.append('mmgrid/mmGrid.js')
    a.append('mmgrid/mmTreeGrid.css')
    a.append('mmgrid/mmTreeGrid.js')
    a.append('mmgrid/mmGanttGrid.css')
    a.append('mmgrid/mmGanttGrid.js')
    return {'toplinks':a, 'depends':['jquery', 'json2']}
