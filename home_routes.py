from flask import Blueprint, request, render_template, redirect, url_for

home_routes_bp = Blueprint("home", __name__)

@home_routes_bp.route("/")
@home_routes_bp.route("/home")
def index():
    print("Redirecting to /stocks/form...")
    return redirect(url_for("dashboard_routes.stocks_form"))  # redirect to your stocks form

@home_routes_bp.route("/about")
def about():
    print("ABOUT...")
    return render_template("about.html")  # keep rendering your template


