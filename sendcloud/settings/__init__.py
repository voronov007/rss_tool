from .base import *  # noqa

env = os.getenv("ENVIRONMENT", "develop").lower()  # base == develop
if env == "test":
    from .test import *  # noqa
elif env == "production":
    from .production import *  # noqa
