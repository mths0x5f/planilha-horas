# API ==========================================================================

import flask

from .associados import AssociadosAPIController
from .eventos import EventosAPIController
from .. import app

api = flask.Blueprint('api', __name__)

add_url = api.add_url_rule

assoc_view = AssociadosAPIController.as_view('associados')
add_url('/associados', view_func=assoc_view, methods=['GET', 'POST', 'DELETE'])
add_url('/associados/<matricula>', view_func=assoc_view,
        methods=['GET', 'PUT', 'DELETE'])

env_view = EventosAPIController.as_view('eventos')
add_url('/eventos', view_func=env_view, methods=['GET', 'POST', 'DELETE'])
add_url('/eventos/<id>', view_func=env_view, methods=['GET', 'PUT', 'DELETE'])

app.register_blueprint(api, url_prefix='/api')

app.config["JSON_SORT_KEYS"] = False


@api.errorhandler(400)
@api.errorhandler(404)
@api.errorhandler(405)
@api.errorhandler(409)
def error_4xx(error):
    message = {404: 'Resource not found',
               409: 'Resource already exists'}
    response = {'error': error.name,
                'message': message.get(error.code, error.description)}
    return flask.make_response(flask.jsonify(response), error.code)
