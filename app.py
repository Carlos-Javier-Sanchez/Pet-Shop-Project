import os
import random
import flask
from flask import Flask, flash, redirect, render_template, \
     request
import sqlite3


app = Flask(__name__)
#'This is NOT a good practice for Secret_key (just for study purpose only)
app.secret_key = ("YOUDONOTSETSECRETKEYHERE")

def get_items():
    # Retrieving items from database to HTML
    get_items.__init__
    sql_cnx = sqlite3.connect('Petshop.db')
    cursor = sql_cnx.cursor()
    query = "Select product_name, Unit_of_measure, price_per_unit from products"
    cursor.execute(query)
    all_data = cursor.fetchall()
    all_data =[val[-3] for val in all_data]

    #Filling shopping list with some items (Just for test program)
    shopping_list = all_data.copy()
    random.shuffle(shopping_list)
    shopping_list = shopping_list[:5]

    return all_data, shopping_list

# ==> to HTML , Main rout
@app.route('/templates/index.html', methods=["POST" ,"GET"])
#set for HTML index
def index():
    flask.session["all_items"], flask.session["shopping_list"] = get_items()
    #flash("Listing Pet shop Items")
    return render_template('index.html', all_items=flask.session["all_items"],
                           shopping_list=flask.session["shopping_list"])

@app.route("/add_items/" , methods=["post"])
def add_items():
    flask.session["shopping_list"].append(flask.request.form["selected_items"])
    flask.session.modified = True
    return render_template('index.html', all_items=flask.session["all_items"],
                          shopping_list=flask.session["shopping_list"])


@app.route("/remove_items/" ,methods=["post"])
def remove_items():
    checked_boxes = request.form.getlist("check")
    for item in checked_boxes:
        if item in flask.session["shopping_list"]:
            idx=flask.session["shopping_list"].index(item)
            flask.session["shopping_list"].pop(idx)
            flask.session.modified = True
    return render_template('index.html', all_items=flask.session["all_items"],
                           shopping_list=flask.session["shopping_list"])


if __name__ == '__main__':
    app.run(debug=True)

#handling listing button - Fetch items
#@app.route("/listing")
#def listing():
#    all_data = get_product()
#    flash("Listing from button  Petshop Items !!!" )
#    return render_template("index.html")



