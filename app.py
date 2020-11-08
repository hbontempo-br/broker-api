import logging  # noqa: E402

import falcon  # noqa: E402
from api.adapters.sink import SinkAdapter  # noqa: E402
from api.resources.home import Home  # noqa: E402
from middleware.input_output import InputOutputMiddleware  # noqa: E402
from middleware.request_track import RequestTrackMiddleware  # noqa: E402
from utils.logger import BaseLogger

# Logger is started here because it needs to run before packages have their own logging
# configuration and invalidates this customization
BaseLogger().config()


def create() -> falcon.API:
    api = falcon.API(middleware=[RequestTrackMiddleware(), InputOutputMiddleware()])

    # mongo_connector = MongoDbConnector()
    # mongo_client = mongo_connector.connect()

    api.add_route(uri_template="/", resource=Home())

    # validator = Registration(mongo_client=mongo_client)
    # api.add_route(uri_template="/registration", resource=validator)
    # api.add_route(
    #     uri_template="/registration/{social_security_number}",
    #     resource=validator,
    #     suffix="with_social_security_number",
    # )

    api.add_sink(SinkAdapter(), r"/")

    logging.debug("Application loaded to worker. Ready to accept requests")

    return api


app = application = create()
