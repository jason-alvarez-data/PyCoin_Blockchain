import argparse
from api.routes import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a blockchain node')
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=True)