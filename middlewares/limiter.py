from flask_jwt_extended import get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import User
from config.extensions import db
from sqlalchemy import select

limiter = Limiter(
    key_func=get_remote_address,
    meta_limits=["2/hour, 4/day"],
    application_limits_exempt_when=lambda: get_jwt_identity() == 1
)