import os
import logging

from flask import Flask, g, request

from .factory import (
    create_celery,
    create_flask_app,
    init_flask_app,
    babel,
    oss,
    gs_vision,
)

from app.constants.locale import Locale
from app.utils.logging import configure_root_logger, configure_extra_logs

configure_root_logger()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 基本路径
APP_PATH = os.path.abspath(os.path.dirname(__file__))
FILE_PATH = os.path.abspath(os.path.join(APP_PATH, "..", "files"))  # 一般文件
TMP_PATH = os.path.abspath(os.path.join(FILE_PATH, "tmp"))  # 临时文件存放地址
STORAGE_PATH = os.path.abspath(os.path.join(APP_PATH, "..", "storage"))  # 储存地址

# Singletons
flask_app = create_flask_app(Flask(__name__))
configure_extra_logs(flask_app)
celery = create_celery(flask_app)
init_flask_app(flask_app)


def create_app():
    return flask_app


@babel.localeselector
def get_locale():
    current_user = g.get("current_user")
    if (
        current_user
        and current_user.locale
        and current_user.locale != "auto"
        and current_user.locale in Locale.ids()
    ):
        return current_user.locale
    return request.accept_languages.best_match(["zh_CN", "zh_TW", "zh", "en_US", "en"])


# @babel.timezoneselector
# def get_timezone():
#     # TODO 弄清 timezone 是什么东西
#     current_user = g.get('current_user')
#     if current_user:
#         if current_user.timezone:
#             return current_user.timezone

__all__ = [
    "oss",
    "gs_vision",
    "flask_app",
    "celery",
    "APP_PATH",
    "STORAGE_PATH",
    "TMP_PATH",
    "FILE_PATH",
]
