from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException

class URLs():
    '''
    The class that holds the url map and the dispatcher.
    
    TODO: dynamically populate it using the manifest.yaml
    '''

    map = Map([
        Rule('/',              endpoint='index'),
        Rule('/users',         endpoint='users'),
        Rule('/users/<id>',    endpoint='user'),
        Rule('/programs/',     endpoint='programs'),
        Rule('/programs/<id>', endpoint='program'),
        Rule('/sets/',         endpoint='sets'),
        Rule('/sets/<id>',     endpoint='set'),
        Rule('/moments/',      endpoint='moments'),
        Rule('/moments/<id>',  endpoint='moment'),
        Rule('/answers/',      endpoint='answers'),
        Rule('/answers/<id>',  endpoint='answer')
    ])
    
    def dispatch(self, request):
        adapter = self.map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, endpoint)(request, **values)
        except HTTPException, e:
            return e
    
    def index(self, request, **kwargs):
        pass
    def users(self, request, **kwargs):
        pass
    def user(self, request, **kwargs):
        pass
    def programs(self, request, **kwargs):
        pass
    def program(self, request, **kwargs):
        pass
    def sets(self, request, **kwargs):
        pass
    def set(self, request, **kwargs):
        pass
    def moments(self, request, **kwargs):
        pass
    def moment(self, request, **kwargs):
        pass
    def answers(self, request, **kwargs):
        pass
    def answer(self, request, **kwargs):
        pass

