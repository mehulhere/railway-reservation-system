import numpy as np
import difflib
from flask import Flask, render_template
from flask_executor import Executor
app = Flask(__name__)
executor = Executor(app)
id=0
itemlist= b = np.load('newarr.npy')
"""
def newitem():
    i1=input("Product")
    i2=int(input("Pcs/Crate"))
    i3=int(input("Rate"))
    newitemlist=[[i1, i2, i3]]
    newarr=np.array(np.append(itemlist,newitemlist,axis=0))
    np.save('newarr.npy', newarr)
    print("the file contains:")
    print(newarr)
def mainmenu(i):
    if i == 1:
        search()
    elif i == 2:
        print("NOT AVAILABLE RN")
    elif i == 3: 
        newitem()
print("Welcome to Billing App")
print("1. Search")
print("2. Transaction")
print("3. New Item")
i=int(input("Enter: "))
def search():
    global itemnamelist
    itemnamelist=[i[0] for i in itemlist]
    print(itemnamelist)
    iname=input("Search: ")
    print(difflib.get_close_matches(iname, itemnamelist))
mainmenu(i)
"""
@app.route("/")
def homepage():
        return render_template('hello.html')
@app.route("/<search>")
def productpage(search):
        return render_template('new.html',search=search)
if __name__== "__main__":
    app.run(debug=True)