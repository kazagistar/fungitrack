#!python2
from flask import Flask, g, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    with app.db.connection() as cnx:
        return render_template('layout.html')



if __name__ == "__main__":
    # Parse command line arguments
    from argparse import ArgumentParser
    parser = ArgumentParser(
    	description='Web server for mushroom gathering data collection',
    	epilog='Easy config setup advice: copy and modify existing .json to config.json')
    parser.add_argument('-c', '--config',
        help='Load configuration from alternate file',
        default='config.json')
    args = parser.parse_args()

    # Read config
    import json
    with open(args.config) as config_file:
        config = json.loads(config_file.read())

    # Database initialization
    from database import get_database
    app.db = get_database(config)

    # Run server
    params = {
        'debug': config.get('debug', False),
        'port': config.get('port', 5000)
    }
    app.run(**params)
