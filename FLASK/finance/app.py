import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import pytz

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    # Get the user's ID from the session
    user_id = session["user_id"]

    # Query the database to get the user's portfolio, including stocks they own and the number of shares owned
    portfolio = db.execute(
        "SELECT symbol, SUM(shares) AS total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0",
        user_id,
    )

    # Create a list to store the user's portfolio data
    portfolio_data = []

    # Calculate the total value of each stock in the portfolio and store the data
    total_portfolio_value = 0
    for stock in portfolio:
        symbol = stock["symbol"]
        shares = stock["total_shares"]
        quote_info = lookup(symbol)

        if quote_info:
            price = quote_info["price"]
            total_value = price * shares
            portfolio_data.append(
                {
                    "symbol": symbol,
                    "name": quote_info["name"],
                    "shares": shares,
                    "price": price,
                    "total_value": total_value,
                }
            )
            total_portfolio_value += total_value

    # Query the database to get the user's current cash balance
    cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

    # Calculate the grand total (total portfolio value + cash balance)
    grand_total = total_portfolio_value + cash_balance

    # Render the index.html template with the portfolio and financial data
    return render_template(
        "index.html",
        portfolio_data=portfolio_data,
        cash_balance=cash_balance,
        grand_total=grand_total,
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        # Ensure a stock symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol")

        # Ensure a valid stock symbol is provided
        quoted = lookup(symbol)
        if not quoted:
            return apology("invalid stock symbol")

        # Ensure a positive integer number of shares was provided
        shares = request.form.get("shares")
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a valid number of shares")

        # Calculate the total cost of the shares
        shares = int(shares)
        total_cost = shares * quoted["price"]

        # Check if the user has enough cash to buy the shares
        user_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]["cash"]
        if user_cash < total_cost:
            return apology("not enough cash to buy the shares")

        # Record the purchase in the database
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, transaction_type, total_cost, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
            session["user_id"],
            symbol,
            shares,
            quoted["price"],
            "BUY",  # Set transaction_type to 'BUY'
            total_cost,
            datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),  # Add a timestamp for the transaction
        )

        # Update the user's cash balance
        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total_cost,
            session["user_id"],
        )

        # Redirect the user to the home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get the user's ID from the session
    user_id = session["user_id"]

    # Query the database to get the user's transaction history
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC", user_id
    )

    # Render the history.html template with the transaction history
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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    """Get stock quote"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure a stock symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol")

        # Get the stock quote using the lookup function
        quoted = lookup(symbol)

        if not quoted:
            return apology("invalid stock symbol")

        # Render the quoted.html template with the stock quote
        return render_template("quoted.html", quoted=quoted)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted and doesn't already exist
        username = request.form.get("username")
        if not username:
            return apology("must provide username")

        # Query database to check if the username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            return apology("username already exists")

        # Ensure password and confirmation were submitted and match
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or password != confirmation:
            return apology("passwords must match")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the new user into the database
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            hashed_password,
        )

        # Redirect user to login page after successful registration
        flash("Registration successful! Please log in.")
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        # Ensure symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares were submitted as a positive integer
        try:
            shares = int(request.form.get("shares"))
            if shares <= 0:
                return apology("number of shares must be a positive integer", 400)
        except ValueError:
            return apology("number of shares must be a positive integer", 400)

        # Lookup the stock symbol
        quote_info = lookup(symbol)
        if not quote_info:
            return apology("symbol not found", 400)

        # Get the user's ID from the session
        user_id = session["user_id"]

        # Query the database to check if the user owns enough shares to sell
        user_shares = db.execute(
            "SELECT SUM(shares) AS total_shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol",
            user_id,
            symbol,
        )

        if not user_shares or user_shares[0]["total_shares"] < shares:
            return apology("not enough shares to sell", 400)

        # Calculate the total value of the sale
        total_value = quote_info["price"] * shares

        # Insert the transaction into the database with 'SELL' as transaction_type
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price, transaction_type, total_cost) VALUES (?, ?, ?, ?, ?, ?)",
            user_id,
            symbol,
            -shares,
            quote_info["price"],
            "SELL",
            total_value,
        )

        # Update the user's cash balance
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?", total_value, user_id
        )

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("sell.html")


# Personal Touch: Change Password
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change user's password"""
    if request.method == "POST":
        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password", 400)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Query database for the user's current password hash
        user_id = session["user_id"]
        user_info = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure old password is correct
        if not check_password_hash(
            user_info[0]["hash"], request.form.get("old_password")
        ):
            return apology("old password is incorrect", 400)

        # Hash the new password
        new_hashed_password = generate_password_hash(request.form.get("new_password"))

        # Update the user's password in the database
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?", new_hashed_password, user_id
        )

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("change_password.html")
