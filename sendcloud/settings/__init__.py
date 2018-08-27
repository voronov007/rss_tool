from .base import *

env = os.getenv("ENVIRONMENT", "develop").lower()
if env == "test":
    from .test import *
elif env == "production":
    from .production import *
