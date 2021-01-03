import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

#connect_db
def get_db():
    #current_app.logger.info('  DB: Check for db connexion before connexion')
    db = getattr(g, '_db', None)
    if db is None:
        # current_app.logger.info('  DB: No db connexion ... Connect ')
        db = g._db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES)
        # current_app.logger.info('  DB: Connected successfuly to DB')
        
        # sqlite3.Row tells the connection to return rows
        # that behave like dicts.
        # This allows accessing the columns by name.
        g._db.row_factory = sqlite3.Row
        
    return db

def close_db(exception=None):
    # current_app.logger.info('  DB: Check for db connexion before closing ')
    db = getattr(g, '_db', None)
    if db is not None:
        # current_app.logger.info('  DB: Close db connexion')
        db.close()
        # current_app.logger.info('  DB: Connexion to db closed')

def init_db():
    # current_app.logger.info('  DB: First initiation of db from schema.sql')
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    # current_app.logger.info('  DB: database successfuly initiated')

@click.command('init-db')
@with_appcontext 
def init_db_command():
    '''Clear the existing data and create new table'''
    init_db()
    click.echo('Database initialized')

def init_app(app):
    # current_app.logger.info('  DB: Initialisation app')
    current_app.teardown_appcontext(close_db)# app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    current_app.cli.add_command(init_db_command) # app.cli.add_command() adds a new command that can be called with the flask command.

def query_db(query, args=(), one=False):
    # current_app.logger.info('DB : Query started')
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv