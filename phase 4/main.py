from connect import connectDB
from dummy_data import dummy_data
from pymongo import errors


def createCollection(db, collection_name):
    try:
        # If the collection doesn't exist, create it
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        elif collection_name in db.list_collection_names():
            print("Collection already exists")
    except Exception as e:
        print("An error occured: ", e)


def insert_into_collection(db, collection_name, data):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Insert the data into the collection
        result = collection.insert_one(data)

        # Print the inserted document ID
        print("Insertion successfully completed")
        print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")


def read_all_data(db, collection_name):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Use the find method to retrieve all documents
        result = collection.find()

        # Iterate through the documents and print them
        for document in result:
            print(document)

    except Exception as e:
        print(f"An error occurred: {e}")


def find_records_containing_item(db, collection_name, item_name):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find orders containing the specified item
        query = {"items.item_name": item_name}

        # Use the find method to retrieve matching documents
        cursor = collection.find(query)

        # Convert your cursor to a list to freely operate over it
        result = list(cursor)

        # Print the matching documents
        for document in result:
            print(document)

        # Return the whole result list
        return result

    except Exception as e:
        print(f"An error occurred: {e}")


def delete_record_by_id(db, collection_name, record_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"customer_id": record_id}

        # Use the delete_one method to delete the document
        result = collection.delete_one(query)

        # Check if the deletion was successful
        if result.deleted_count == 1:
            print(f"Successfully deleted record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def update_record_list_by_id(db, collection_name, record_id, new_order_list):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"customer_id": record_id}

        # Use the update_one method to update the specific field (order_list)
        result = collection.update_one(query, {"$set": {"items": new_order_list}})

        # Check if the update was successful
        if result.matched_count == 1:
            print(f"Successfully updated order_list for record with ID {record_id}")
        else:
            print(f"No record found with ID {record_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")


def delete_record_by_item(db, collection_name, item="Pizza"):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"items.item_name": item}

        # Use the delete_one method to delete the document
        result = collection.delete_many(query)

        # Check if the deletion was successful
        if result.deleted_count >= 1:
            print(
                f"Successfully deleted {result.deleted_count} record that contains {item}"
            )
        else:
            print(f"No record found with {item}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def get_new_item_list_input():
    new_order_list = []
    while True:
        item_name = input("Enter item name (or 'done' to finish): ")
        if item_name.lower() == "done":
            break
        new_order_list.append({"item_name": item_name})

    return new_order_list

if __name__ == "__main__":
    # First create a connection
    db = connectDB()

    # Then create a collection
    createCollection(db, "favorites")
    createCollection(db, "wantlist")

    found_documents = find_records_containing_item(
        db, collection_name="favorites", item_name="Gta 6"
    )

    # # Delete the first record which has a pizza in its order list
    id_to_delete = found_documents[0]["_id"]
    print(id_to_delete)

    # # Insert some dummy data into your collection
    """"
    for item in dummy_data:
        insert_into_collection(db, "favorites", item)
    for item in dummy_data:
        insert_into_collection(db, "wantlist", item)
    """

    print("Welcome to Review Portal!")
    print("Please enter your user id:")
    user_id = input()
    while True:
        print("Please pick the option that you want to proceed.")
        print("1- Create a collection.")
        print("2- Read all data in a collection.")
        print("3- Read some part of the data while filtering.")
        print("4- Insert data.")
        print("5- Delete data.")
        print("6- Update data.")
        print("Selected option: ")
        option = input()

        if option == "1":
            print("Please enter the collection name you want to create:")
            collection_name = input()
            createCollection(db, collection_name)

        elif option == "2":
            print("Please enter the collection name to read all data:")
            collection_name = input()
            read_all_data(db, collection_name)

        elif option == "3":
            print("Please enter the collection name to filter data:")
            collection_name = input()
            print("Please enter the item name to filter:")
            item_name = input()
            find_records_containing_item(db, collection_name, item_name)

        elif option == "4":
            print("Please select the collection you want to insert data:")
            print("1- Favorites")
            print("2- Wanted list")
            selected_collection = input()

            if selected_collection == "1":
                collection_name = "favorites"
            elif selected_collection == "2":
                collection_name = "wantedlist"
            else:
                print("Invalid selection")
                continue

            print("Please enter the data fields:")
            id = input("costumer_id: ")
            name = input("costumer_name: ")
            item_list = get_new_item_list_input()

            data = {
                "costumer_id": id,
                "costumer_name": name,
                "items" : item_list
            }

            insert_into_collection(db, collection_name, data)
            print("The data was successfully inserted!")

        elif option == "5":
            print("Please enter the collection name to delete data:")
            collection_name = input()
            print("Please select delete option (id/item):")
            delete_option = input()
            if(delete_option == "id"):
                print("Please enter the record id to delete:")
                record_id = input()
                delete_record_by_id(db, collection_name, record_id)
            elif(delete_option == "item"):
                print("Please enter the record name to delete:")
                item_name = input()
                delete_record_by_item(db, collection_name, item_name)

        elif option == "6":
            print("Please enter the collection name to update data:")
            collection_name = input()
            print("Please enter the record ID to update:")
            record_id = input()
            print("Please enter the new item")
            new_item = get_new_item_list_input()
            update_record_list_by_id(db, collection_name, record_id, new_item)

        print("\nWhat would you like to do next?")