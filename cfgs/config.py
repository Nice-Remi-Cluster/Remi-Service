FastapiHost = "127.0.0.1"
FastapiPort = 8000
DatabaseUrl = "sqlite://db.sqlite3"

TORTOISE_ORM = {
    "connections": {"default": "sqlite://data/db.sqlite3"},
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

# CasbinDB = "mysql+aiomysql://user:pwd@127.0.0.1:3306/exampledb"
CasbinPolicyPath = "cfgs/casbin_policy.csv"
CasbinModelPath = "cfgs/casbin_model.conf"
