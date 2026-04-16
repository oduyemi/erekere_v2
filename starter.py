from ereapp import starter

if not starter.config['MONGO_URI']:
    raise ValueError("MONGO_URI is not set")

if __name__ == "__main__":
    starter.run(debug = True)































if __name__ == '__main__':
    starter.run(debug = True, port = 8500)