#coding:utf-8
import json
import web

from models import Todos

# 添加todo相关的urls
urls = (
    '/', 'index',  #返回首页
    '/todo/', 'todo',  #  处理POST请求
    '/todo/(\d+)', 'todo',  # 处理前端todo的请求,对指定记录进行操作
    '/todos/', 'todos',  # 处理前端todo的请求，返回所有数据
)
app = web.application(urls, globals())

render = web.template.render('')

class index:
    def GET(self):
        return render.index()

#添加接口的处理代码
class todo:
    def GET(self, todo_id=None):
        result = None
        todo = Todos.get_by_id(id=todo_id)
        # return json.dumps(todo._order)
        # 先用这种比较傻的方式
        result = {
            "id": todo.id,
            "title": todo.title,
            "order": todo._order,
            "done": todo.done == 1,
        }
        return json.dumps(result)

    def POST(self):
        data = web.data()
        todo = json.loads(data)
        todo['_order'] = todo.pop('order')
        Todos.create(**todo)

    def PUT(self, todo_id=None):
        data = web.data()
        todo = json.loads(data)
        todo['_order'] = todo.pop('order')
        Todos.update(**todo)
    def DELETE(self, todo_id=None):
        Todos.delete(id=todo_id)

#处理整体的请求
class todos:
    def GET(self):
        todos = []
        itertodos = Todos.get_all()
        for todo in itertodos:
            todos.append({
                "id": todo.id,
                "title": todo.title,
                "order": todo._order,
                "done": todo.done == 1,
            })
        return json.dumps(todos)


if __name__ == "__main__":
    app.run()