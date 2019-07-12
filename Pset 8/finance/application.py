# semi-done

# lookup function does not work and to fix that CS50 lead me to a website to register where I literally cant click on the register button - making it uncheckable
# https://cs50.stackexchange.com/questions/32823/my-cs50-finance-lookup-stopped-working-on-15-jun-2019-is-there-trouble-with-the
# as a consequence check50 also doesn't work - largely built upon other's code - only struggled with it for completeness

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    portfolio = db.execute("SELECT symbol, SUM(shares) as number_of_shares, price FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])

    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

    available_cash = rows[0]["cash"]

    return render_template("index.html", portfolio=portfolio, available_cash=available_cash)
    
    


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    
    if request.method == "POST":
        
        stock = lookup(request.form.get("symbol"))
        
        if stock == None:
            return apology("invalid symbol")
        
        
        ###########################
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must be a number")
        
        if shares < 0:
            return apology("must be a positive number")
        
        rows = db.execute("SELECT cash FROM users WHERE id =:user_id", user_id=session["user_id"])              ############################################
        
        available_cash = rows[0]["cash"]            ###############################
        price = stock["price"]      # assumes lookup returns a JSON
        total_price = shares * price
        
        if available_cash < total_price:
            return apology("insufficient funds")
        
        
        
        db.execute("UPDATE users SET cash = cash - :total_price WHERE id = :user_id", total_price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO 'transactions' (user_id, symbol, shares, price) VALUES (:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=request.form.get("symbol"), shares=shares, price=price)
        
        return redirect("/")
    
    
    return apology("TODO")
    


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.form.get("username")
    if (len(username) > 0) or (len(db.execute("SELECT * FROM users WHERE username = :username", username=username)) == 0):
        return jsonify(True)        #isnt this works with lowercase letters?
    else:
        return jsonify(False)
    #return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("SELECT symbol, shares, price, timestamp FROM transactions WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    elif request.method == "POST":
        quote = lookup(request.form.get("symbol"))
        if quote == None:   #stock is valid ?
            return apology("stock is not valid")
        else:
            return render_template("quoted.html", quote=quote)
    else:
        return apology("TODO")






@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        #
        if (not request.form.get("username")) or (not request.form.get("password")) or (not request.form.get("confirmation")):
            return apology("blank space")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")
        
        # hash password
        password = request.form.get("password")
        hash = generate_password_hash(password)
        
        # INSERT
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=request.form.get("username"), hash=hash)
        # elif username already exist
        if not result:
            return apology("username is taken")     # Because usernames are a UNIQUE field in the database
        
        # log them in
        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        return redirect("/")
    
    else:
        return apology("TODO")
    
    




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))

        if stock == None:
            return apology("invalid ticker symbol")

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must be a number")

        if shares < 0:
            return apology("input positive number")

        available_shares = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id and symbol = :symbol GROUP BY symbol",
                                        user_id=session["user_id"], symbol=request.form.get("symbol"))

        if available_shares[0]["total_shares"] < 1 or shares > available_shares[0]["total_shares"]:
            return apology("not enough shares")

        price = stock["price"]

        total_price = shares * price

        db.execute("UPDATE users SET cash = cash + :total_price WHERE id = :user_id", user_id=session["user_id"], total_price=total_price)
        db.execute("INSERT INTO 'transactions' (user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)", user_id=session["user_id"], symbol=request.form.get("symbol"), shares=-shares, price=price)

        return redirect("/")

    else:
        available_stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol", user_id=session["user_id"])
        return render_template("sell.html", available_stocks=available_stocks)
    
    
    
@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Changes Password"""

    if request.method == "GET":
        return render_template("password.html")

    elif request.method == "POST":
        if not request.form.get("old_password"):
            return apology("must provide old password")
        elif not request.form.get("new_password"):
            return apology("must provide new password")
        elif not request.form.get("confirmation"):
            return apology("must provide new password again")
        
        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("(new) passwords must match")
        
        hashes = db.execute("SELECT hash FROM users WHERE id = :id", id=session['user_id'])
        
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
        # hashes != generate_password_hash(request.form.get("old_password")):     # [0]["hash"]
        # if not pwd_context.verify(request.form.get("old_password"), hashes[0]["hash"]):           # shit function
            return apology("wrong (old) password")
            
#             # Query database for username
#        rows = db.execute("SELECT * FROM users WHERE username = :username",
#                          username=request.form.get("username"))
#
#        # Ensure username exists and password is correct
#        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
#            return apology("invalid username and/or password", 403)
        
        db.execute("UPDATE users SET hash = :hash WHERE id=:id", hash=generate_password_hash(request.form.get("new_password")), id=session["user_id"] )
        flash("password changed successfully")
        
        return redirect(url_for("index"))
        
    else:
        return apology("Could not change password")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
