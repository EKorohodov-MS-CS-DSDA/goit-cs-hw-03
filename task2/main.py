from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError

client = MongoClient("mongodb+srv://eduardkorohodov:VPLFxu6hXMCjnsvr@cluster0.3zxe7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
                     , server_api=ServerApi('1'))

db = client.hw_03

class CatData:
    name = ''
    age = 0
    features = []

    def __init__(self, name, age, features):
        self.name = name
        self.age = age
        self.features = features

    def __repr__(self):
        return f"{self.name} {self.age} {self.features}"

def add_cats(cats: list[CatData]):
    """
    Adds a list of CatData objects to the cats collection.
    """

    try:
        result = db.cats.insert_many([cat.__dict__ for cat in cats])
        print(f"Added {len(result.inserted_ids)} documents")
    except PyMongoError as e:
        print(e)

def add_cat(cat: CatData):
    """
    Adds a CatData object to the cats collection.
    """

    try:
        result = db.cats.insert_one(cat.__dict__)
        print("Operation Successful." if result.inserted_id > 0 else "Operation failed.")
    except PyMongoError as e:
        print(e)

def get_all_cats():
    """
    Finds all documents in the cats collection and prints them out.
    """

    try:
        result = db.cats.find({})
        for el in result:
            print(el)
    except PyMongoError as e:
        print(e)

def get_cat_by_name(name):
    """
    Finds a document in the cats collection by name and prints it out.
    """

    try:
        result = db.cats.find_one({'name': name})
        print(result)
    except PyMongoError as e:
        print(e)

def update_cat_age(name, age):
    """
    Updates the age of a document in the cats collection by name.
    """

    try:
        result = db.cats.update_one({'name': name}, {'$set': {'age': age}})
        print("Operation Successful." if result.modified_count > 0 else "Operation failed.")
    except PyMongoError as e:
        print(e)

def add_cat_features(name, features):
    """
    Adds features to a cat document in the cats collection by name.
    Prints the updated document if the operation is successful.
    """

    try:
        result = db.cats.update_one({'name': name}, {'$addToSet': {'features': {'$each': features}}})
        if result.modified_count > 0:
            print(db.cats.find_one({'name': name}))
        else:
            print("Operation failed.")
    except PyMongoError as e:
        print(e)

def delete_cat(name):
    """
    Deletes a document in the cats collection by name.
    """

    try:
        result = db.cats.delete_one({'name': name})
        print("Operation Successful." if result.deleted_count > 0 else "Operation failed.")
    except PyMongoError as e:
        print(e)

def delete_all_cats():
    """
    Deletes all documents in the cats collection.
    """

    try:
        result = db.cats.delete_many({})
        print("Operation Successful." if result.deleted_count > 0 else "Operation failed.")
    except PyMongoError as e:
        print(e)


def get_help_info():
    """Prints help information about commands"""
    print("""
          add_cat <name> <age> <features separated by commas> - add new cat
          get_all_cats - get all cats
          get_cat_by_name <name> - get a cat by name
          update_cat_age <name> <age> - update cat age
          add_cat_features <name> <features separated by commas> - add cat features
          delete_cat <name> - delete cat
          delete_all_cats - delete all cats
          exit - to exit
          help - to see this message again
          """)


def concat_features(tokens):
    """
    Groups tokens into cats' features

    Args:
        tokens (list): list of tokens to group up

    Returns:
        list: list of features
    """
    tokens_concat = ' '.join(tokens)
    feature_tokens = tokens_concat.split(',')
    return [feature.strip() for feature in feature_tokens]


def process_command(line: str):
    """
    Processes a given command line and executes the corresponding action

    Args:
        line (str): command line to process
    """
    if len(line) == 0:
        return

    try:
        tokens = line.split()
        command = tokens.pop(0)

        match command:
            case 'add_cat':
                features = concat_features(tokens[2:])
                add_cat(CatData(tokens[0], int(tokens[1]), features))
            case 'get_all_cats':
                get_all_cats()
            case 'get_cat_by_name':
                get_cat_by_name(tokens[0])
            case 'update_cat_age':
                update_cat_age(tokens[0], int(tokens[1]))
            case 'add_cat_features':
                features = concat_features(tokens[1:])
                add_cat_features(tokens[0], features)
            case 'delete_cat':
                delete_cat(tokens[0])
            case 'delete_all_cats':
                delete_all_cats()
            case 'help':
                get_help_info()
            case _:
                print("type 'help' for the commands list")
    except Exception as e:
        print(e)

def main():
    # run the comms loop
    print("Welcome to cats database")
    print("type 'help' for the commands list")

    while True:
        line = input(">: ")
        if line == 'exit':
            break
        else:
            process_command(line)

    print("Goodbye")

if __name__ == "__main__":
    # reset db and populate it with default data
    delete_all_cats()
    cats = [CatData('Barsik', 3, ['ходить в капці', 'дає себе гладити', 'рудий']),
            CatData('Lama', 2, ['ходить в лоток', 'не дає себе гладити', 'сірий']),
            CatData('Liza', 4, ['ходить в лоток', 'дає себе гладити', 'білий'])]
    add_cats(cats)

    main()
