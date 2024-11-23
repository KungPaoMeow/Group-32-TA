from datetime import date, datetime
from flask import Flask, render_template, request, redirect, jsonify
from pymongo_get_db import MongoDB
from bson.objectid import ObjectId
from datetime import datetime


app = Flask(__name__)
db_service = MongoDB()
db = db_service.db

drug_inv_collection = db["drugs"]
order_collection = db["orders"]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('dashboard.html', user_input=None)

@app.route('/dashboard')
def dashboard():
    total_orders = order_collection.count_documents({})
    drug_inventory = drug_inv_collection.count_documents({})
    earnings = 123114

    # Testing creating a collection under the DB and inserting a record
    dashboard_data = {
        'total_orders' : total_orders,
        'drug_inventory' : drug_inventory,
        'earnings' : earnings
    }
    test_collection = db["dashboard"]
    existing_record = test_collection.find_one({"total_orders": total_orders, "drug_inventory": drug_inventory})
    if not existing_record:
        test_collection.insert_one(dashboard_data)
        print("New dashboard data inserted.")
    else:
        print("Dashboard data already exists, skipping insertion.")
    orders = list(order_collection.find())
    return render_template('dashboard.html', total_orders=total_orders, drug_inventory=drug_inventory, earnings=earnings, orders=orders)


### Currently unused ###
@app.route('/add-sample-drug')
def add_sample_drug():
    # Define drug data to be inserted directly in the code
    drug_data = {
        "name": "Sample Drug",
        "company": "Sample Company",
        "type": "Prescription",
        "description": "This is a sample drug used for testing.",
        "stock": 50
    }
    
    # Check if the drug already exists to avoid duplicate insertion
    existing_drug = drug_inv_collection.find_one({"name": drug_data["name"]})
    
    if existing_drug:
        return jsonify({"msg": "Drug already exists in the database.", "id": str(existing_drug["_id"])}), 409
    else:
        # Insert new drug data
        inserted_id = drug_inv_collection.insert_one(drug_data).inserted_id
        return jsonify({"msg": "Drug added successfully", "id": str(inserted_id)}), 201


@app.route('/inv-monitoring')
def drug_table():
    # list of drugs to be displayed on inventory monitoring page
    drugs = list(drug_inv_collection.find())
    return render_template('inv-monitoring.html', drugs=drugs)

@app.route('/browse-drug')
def browse_drug():
    drugs = list(drug_inv_collection.find())
    return render_template('browse-drug.html', drugs=drugs)

@app.route('/drug-edit/<id>', methods=['GET', 'POST'])
def drug_edit(id):
    # get the info of the selected drug
    print(f"Received ID: {id} (type: {type(id)})")  # Debugging received ID
    try:
        drug = drug_inv_collection.find_one({"_id": ObjectId(id)})
        print(f"Drug found: {drug}")  # Debugging database query result
    except Exception as e:
        print(f"Error during database query: {e}")
        return "Drug not found", 404
    
    if not drug:
        return "Drug not found", 404
    
    if request.method == 'POST':
        # update the drug info
        drug['name'] = request.form['name']
        drug['company'] = request.form['company']
        drug['type'] = request.form['type']
        drug['description'] = request.form['description']
        drug['stock'] = request.form['stock']

        # flask automatically converts form data to strings apparently, so convert it back to int
        try:
             drug['stock'] = int( drug['stock'])
        except ValueError:
            return "Invalid stock value", 400
        
        # update the drug in the db
        drug_inv_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "name": drug['name'],
                "company": drug['company'],
                "type": drug['type'],
                "description": drug['description'],
                "stock": drug['stock']
            }}
        )

        if request.args.get('from') == 'info':
            return redirect('/drug-info')
        # send the user back to inventory monitoring page
        return redirect('/inv-monitoring')
    # display the drug info
    return render_template('drug-edit.html', drug=drug)
    
@app.route('/new-drug', methods=['GET', 'POST'])
def new_drug():
    # initialize the new drug to add
    drug = {"name": "", "company": "", "type": "", "stock": 0}
    if request.method == 'POST':
        # add the user-provided drug info to the list
        drug['name'] = request.form['name']
        drug['company'] = request.form['company']
        drug['type'] = request.form['type']
        drug['description'] = request.form['description']
        drug['stock'] = request.form['stock']

        # flask automatically converts form data to strings apparently, so convert it back to int
        try:
             drug['stock'] = int( drug['stock'])
        except ValueError:
            return "Invalid stock value", 400
        
        drug_inv_collection.insert_one(drug)
        # drugs.append(drug)

        if request.args.get('from') == 'info':
            return redirect('/drug-info')
        # send the user back to inventory monitoring page
        return redirect('/inv-monitoring')
    
    # show form to add a drug
    return render_template('new-drug.html')

@app.route('/delete-drug/<id>', methods=['GET','POST'])
def delete_drug(id):
    drug = drug_inv_collection.find_one({"_id": ObjectId(id)})
    if not drug:
        return "Drug not found", 404
    
    if request.method == 'POST':
        if request.form['delete'] == 'Yes':
            # remove drug from list if user confirms that they want to delete it
            drug_inv_collection.delete_one({"_id": ObjectId(id)})
        # send the user back to inventory monitoring page
        return redirect('/inv-monitoring')
    
    # show confirmation page
    return render_template('delete-drug.html', drug=drug)

@app.route('/drug-info', methods=['GET'])
def drug_info():
    drugs = list(drug_inv_collection.find())
    return render_template('drug-info.html', drugs=drugs)

@app.route('/drug-search', methods=['GET'])
def search():
    query = request.args.get('q')
    testing = request.args.get('test')
    collection = list(drug_inv_collection.find())
    if testing:
        collection = list(db[testing].find())

    filtered_drugs = []
    for drug in collection:
        drug_name = drug['name'].lower()
        if query in drug_name:
            filtered_drugs.append(drug_name)
    # Return JSON result that can be used for dynamic updates with JS
    return jsonify(filtered_drugs)


### Currently unused ###
@app.route('/add-sample-order')
def add_sample_order():
    # Define a sample order with a specific date
    sample_order = {
        "name": "Test Order",
        "date_of_purchase": datetime.strptime("2023-01-15", "%Y-%m-%d"),
        "pickup_or_delivery": "pickup",
        "status": "pending"
    }
    
    # Insert the sample order into the 'orders' collection
    order_collection.insert_one(sample_order)
    return "Sample order added to MongoDB with specified date."


@app.route('/order-tracking')
def order_tracking():
    orders = list(order_collection.find())
    return render_template('order-tracking.html', orders=orders)

@app.route('/new-order', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        new_order_data = {
            "name": request.form['name'],
            "date_of_purchase": request.form['date_of_purchase'],
            "pickup_or_delivery": request.form['pickup_or_delivery'],
            "status": request.form['status']
        }

        # Convert date from string to datetime
        try:
            new_order_data["date_of_purchase"] = datetime.strptime(new_order_data["date_of_purchase"], "%Y-%m-%d").date()
            new_order_data["date_of_purchase"] = str(new_order_data["date_of_purchase"])
        except ValueError:
            return "Invalid date value", 400

        # Insert the new order into MongoDB
        order_collection.insert_one(new_order_data)
        return redirect('/order-tracking')
    
    return render_template('new-order.html')

@app.route('/edit-order/<id>', methods=['GET', 'POST'])
def edit_order(id):
    # Find the order by ID in MongoDB
    order = order_collection.find_one({"_id": ObjectId(id)})
    if not order:
        return "Order not found", 404

    if request.method == 'POST':
        # Update order information
        updated_order = {
            "name": request.form['name'],
            "date_of_purchase": request.form['date_of_purchase'],
            "pickup_or_delivery": request.form['pickup_or_delivery'],
            "status": request.form['status']
        }

        # Convert date from string to datetime
        try:
            updated_order["date_of_purchase"] = datetime.strptime(updated_order["date_of_purchase"], "%Y-%m-%d").date()
            updated_order["date_of_purchase"] = str(updated_order["date_of_purchase"])
        except ValueError:
            return "Invalid date value", 400

        # Update the order in MongoDB
        order_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": updated_order}
        )
        return redirect('/order-tracking')

    return render_template('edit-order.html', order=order)

@app.route('/delete-order/<id>', methods=['GET', 'POST'])
def delete_order(id):
    order = order_collection.find_one({"_id": ObjectId(id)})
    if not order:
        return "Order not found", 404

    if request.method == 'POST':
        if request.form['delete'] == 'Yes':
            # Delete the order from MongoDB
            order_collection.delete_one({"_id": ObjectId(id)})
        return redirect('/order-tracking')
    
    return render_template('delete-order.html', order=order)



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5001, debug=True)
