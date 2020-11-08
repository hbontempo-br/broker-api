# Logger is started here because it needs to run before packages have their own logging
# configuration and invalidates this customization
from utils.logger import BaseLogger  # noqa: E402

BaseLogger().config()  # noqa: E402

import logging  # noqa: E402

import falcon  # noqa: E402
from api.adapters.sink import SinkAdapter  # noqa: E402
from api.resources.home_resource import HomeResource  # noqa: E402
from api.resources.user_resource import UserResource  # noqa: E402
from constants import (  # noqa: E402
    DB_ADDRESS,
    DB_DATABASE,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
)
from middleware.input_output import InputOutputMiddleware  # noqa: E402
from middleware.request_track import RequestTrackMiddleware  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402


def create() -> falcon.API:
    api = falcon.API(middleware=[RequestTrackMiddleware(), InputOutputMiddleware()])

    session_factory = get_db_session_factory()

    api.add_route(uri_template="/", resource=HomeResource())

    user_resource = UserResource(session_factory=session_factory)
    api.add_route("/user", user_resource)
    api.add_route("/user/{user_key}", user_resource, suffix="with_user_key")

    api.add_sink(SinkAdapter(), r"/")

    logging.debug("Application loaded to worker. Ready to accept requests")

    return api


def get_db_session_factory() -> sessionmaker:
    engine = create_engine(
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_DATABASE}"
    )
    engine.connect()
    session_factory = sessionmaker(bind=engine)
    return session_factory


app = application = create()
