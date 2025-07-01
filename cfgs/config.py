FastapiHost = "0.0.0.0"
FastapiPort = 8000
DatabaseUrl = "sqlite://db.sqlite3"

TORTOISE_ORM = {
    "connections": {"default": "mysql://username:password@host:port/database"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}