import utils


def runReader(config, debug=False):
    # Performance Counter Start
    perfStart = utils.performance("start")
    # Get attributes
    attributes = utils.getAttributes("item", debug)
    attributes = utils.sortIterable(attributes)
    attributes = "\n".join(attributes)
    if utils.saveTxt('./output/attributes.txt', attributes):
        # Performance Counter End
        perfStop = utils.performance("end", perfStart)
        print(f"Total elapsed time: {round(perfStop, 3)}s ({round(perfStop / 60, 1)}min)")
    else:
        print("Something went wrong!")


def runParser(config, debug=False):
    # Performance Counter Start
    perfStart = utils.performance("start")
    # Check for database and connect
    link, conn = utils.dbConnect(config)
    # Gather items and display names
    items = {}
    items = utils.itemsRead(items, debug)
    items = utils.itemsAddName(items, debug)
    # Insert data into database
    if utils.itemsInsertDb(items, link, conn):
        # Performance Counter End
        perfStop = utils.performance("end", perfStart)
        print(f"Total elapsed time: {round(perfStop, 3)}s ({round(perfStop / 60, 1)}min)")
    else:
        print("Something went wrong!")
    # Close connection
    conn.close()



if __name__ == '__main__':
    config = utils.readConfig('config.ini')
    debug = True if config['Parser']['debug'] == "True" else False
    runParser(config, debug)
