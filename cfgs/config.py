from httpx import Proxy

FastapiHost = "0.0.0.0"
FastapiPort = 8000

TORTOISE_ORM = {
    "connections": {"default": "mysql://remi-service-dev:u8nI89o6@114.66.61.131:25314/RemiServiceDev"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}