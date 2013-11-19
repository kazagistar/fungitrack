#!python2
from routes import app
import auth

if __name__ == "__main__":
    # Parse command line arguments
    from argparse import ArgumentParser
    parser = ArgumentParser(
        description='Web server for mushroom gathering data collection',
        epilog='Easy config setup advice: copy and modify existing .json to config.json')
    parser.add_argument('-c', '--config',
        help='Load configuration from alternate file',
        default='config.json')
    parser.add_argument('-r','--reload',
        help='Reload db from schema and exit',
        action='store_true')
    args = parser.parse_args()

    # Read config
    import json
    with open(args.config) as config_file:
        config = json.loads(config_file.read())

    # Database initialization
    from database import get_database
    app.db = get_database(config)
    if args.reload:
        app.db.reinitialize()
        quit()

    # Run server
    app.secret_key = 'development key'
    params = {
        'debug': config.get('debug', False),
        'port': config.get('port', 5000)
    }
    app.run(**params)
