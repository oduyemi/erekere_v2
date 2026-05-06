from ereapp import starter as app
# from ereapp import starter
# if not starter.config['MONGO_URI']:
#     raise ValueError("MONGO_URI is not set")

@app.route("/debug")
def debug():
    return {
        "mongo_uri": bool(app.config.get("MONGO_URI")),
        "secret_key": bool(app.config.get("SECRET_KEY")),
    }

if __name__ == "__main__":
    starter.run(debug = True)































if __name__ == '__main__':
    starter.run(debug = True, port = 8500)