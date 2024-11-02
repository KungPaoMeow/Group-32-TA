from datetime import date, datetime
from flask import Flask, render_template, request, redirect, jsonify
from pymongo_get_db import MongoDB
from bson.objectid import ObjectId


app = Flask(__name__)

drug_inv_collection = db["drugs"]

drugs = [
        {"name": "Drug1", "company": "C1", "type": "Prescription", "description": "<insert super long blurb>", "stock": 20},
        {"name": "Drug2", "company": "C2", "type": "Over the Counter", "description": "<insert super long blurb>", "stock": 30},
]
orders = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']
        return render_template('index.html', user_input=user_input)
    return render_template('dashboard.html', user_input=None)

@app.route('/dashboard')
def dashboard():
    total_orders = 888
    drug_inventory = 123974
    earnings = 123114

    order_increase = 201
    inventory_increase = 2100
    earnings_increase = 11981

    return render_template('dashboard.html', 
                           total_orders=total_orders,
                           drug_inventory=drug_inventory,
                           earnings=earnings,
                           order_increase=order_increase,
                           inventory_increase=inventory_increase,
                           earnings_increase=earnings_increase,
                           orders=orders)



@app.route('/inv-monitoring')
def drug_table():
    # list of drugs to be displayed on inventory monitoring page
    drugs = list(drug_inv_collection.find())
    
    return render_template('inv-monitoring.html', drugs=drugs)

@app.route('/drug-edit/<id>', methods=['GET', 'POST'])
def drug_edit(id):
    # get the info of the selected drug
    # drug = drugs[id]
    drug = drug_inv_collection.find_one({"_id": ObjectId(id)})
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
    return render_template('drug-edit.html', drug=drug, ids=range(len(drugs)))
    
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

@app.route('/delete-drug/<int:id>', methods=['GET','POST'])
def delete_drug(id):
    drug = drugs[id]
    if request.method == 'POST':
        if request.form['delete'] == 'Yes':
            # remove drug from list if user confirms that they want to delete it
            drugs.pop(id)
        # send the user back to inventory monitoring page
        return redirect('/inv-monitoring')
    
    # show confirmation page
    return render_template('delete-drug.html', drug=drug)

@app.route('/drug-info', methods=['GET'])
def drug_info():
    return render_template('drug-info.html', drugs=drugs)



@app.route('/order-tracking')
def order_tracking():
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

        # convert date from string to the correct data type
        try:
             new_order_data["date_of_purchase"] = datetime.strptime(new_order_data["date_of_purchase"], "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date value", 400

        orders.append(new_order_data)
        return redirect('/order-tracking')
    return render_template('new-order.html')

@app.route('/edit-order/<int:id>', methods=['GET', 'POST'])
def edit_order(id):
    order = orders[id]
    if request.method == 'POST':
        order['name'] = request.form['name']
        order['date_of_purchase'] = request.form['date_of_purchase']
        order['pickup_or_delivery'] = request.form['pickup_or_delivery']
        order['status'] = request.form['status']

        # convert date from string to the correct data type
        try:
             order["date_of_purchase"] = datetime.strptime(order["date_of_purchase"], "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date value", 400
        return redirect('/order-tracking')
    return render_template('edit-order.html', order=order)

@app.route('/delete-order/<int:id>', methods=['GET', 'POST'])
def delete_order(id):
    order = orders[id]
    if request.method == 'POST':
        if request.form['delete'] == 'Yes':
            orders.pop(id)
        return redirect('/order-tracking')

    return render_template('delete-order.html', order=order)



@app.route('/browse-drug')
def browse_drug():
    return render_template('browse-drug.html', drugs=drugs)



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(port=5001, debug=True)
