import datetime
import utils


def main(config, debug=False):
    perfStart = datetime.datetime.now()

    # Check for database and connect
    link, conn = utils.dbConnect(config)
    # Gather items and display name
    items = {}
    items = utils.itemsRead(items, debug)
    items = utils.itemsAddName(items, debug)
    # Insert data into database
    if utils.itemsInsertDb(items, link, conn):
        perfStop = datetime.datetime.now()
        perfDelta = (perfStop - perfStart).total_seconds()
        perfTime = f"{round(perfDelta, 3)}s ({round(perfDelta / 60, 1)}min)"
        print(f"Total elapsed time: {perfTime}")
    else:
        print("Something went wrong!")
    # Close connection
    conn.close()



if __name__ == '__main__':
    config = utils.readConfig('config.ini')
    debug = True if config['Parser']['debug'] == "True" else False
    main(config, debug)
