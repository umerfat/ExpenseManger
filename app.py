from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file  = "sqlite:///{}".format(os.path.join(project_dir, "expenseDatabase.db"))

app = Flask(__name__)

# Config app to use database
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Expense(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    expenseName = db.Column(db.String(40), nullable=False)
    expenseDate = db.Column(db.String(40), nullable=False)
    expenseAmount = db.Column(db.Integer, nullable=False)
    expenseCategory = db.Column(db.String(40), nullable=False)

# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()

@app.route('/')
def homePage():
    return render_template('displayExpenses.html')

# Add expenses view
@app.route('/add')
def add():
    return render_template('add.html')

# Display expenses view
@app.route('/displayExpenses')
def displayExpenses():
    expenses = Expense.query.all()

    sum=0
    sum_food = 0
    sum_entertainment = 0
    sum_groceries = 0
    sum_sports = 0
    sum_other = 0
    for expense in expenses:
        sum+=expense.expenseAmount
        if (expense.expenseCategory == 'food'):
            sum_food+=expense.expenseAmount
        elif (expense.expenseCategory == 'entertainment'):
            sum_entertainment+=expense.expenseAmount
        elif (expense.expenseCategory == 'groceries'):
            sum_groceries+=expense.expenseAmount
        elif (expense.expenseCategory == 'sports'):
            sum_sports+=expense.expenseAmount 
        elif (expense.expenseCategory == 'other'):
            sum_other+=expense.expenseAmount 

    print(sum_food)
    return render_template('displayExpenses.html', expenses=expenses, sum=sum, sum_food=sum_food,
     sum_entertainment=sum_entertainment, sum_groceries=sum_groceries, sum_sports=sum_sports, sum_other=sum_other)

# Route and view to delete expense
@app.route('/deleteExpense/<int:id>')
def deleteExpense(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect('/displayExpenses')


#Route and view to update expense
@app.route('/updateExpense/<int:id>')
def updateExpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('updateExpense.html', expense = expense)

@app.route('/editExpense', methods=['POST'])
def editExpense():
    id = request.form['id']
    name = request.form['name']
    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']

    #Updated Expense model object data and commit to databse
    db.session.query(Expense).filter_by(id=id).update({"expenseName":name, 
    "expenseDate":date, "expenseAmount":amount, "expenseCategory":category})
    
    db.session.commit()
    return redirect('/displayExpenses')

# View to retrieve data from form and set it db model
@app.route('/addExpense', methods=['POST'])
def addExpense():
    name = request.form['name']
    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']
    #print(name +" "+date+ " " +amount+ " "+ category)

    #initilising database model object/Set value of object('expense') properties to value obtained 
    # from user from details
    expense = Expense(expenseName=name,expenseDate=date, expenseAmount=amount, expenseCategory=category)
    db.session.add(expense)
    db.session.commit()

    return redirect('/displayExpenses')

#app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)