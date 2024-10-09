from flask import render_template, request, redirect, url_for, flash
from eventmanager import app, db
from eventmanager.models import Event, Category  # Import Category along with Event
from datetime import datetime
import os

# Home page showing list of all upcoming and past events
@app.route("/")
def home():
    sort_by = request.args.get("sort_by", "date")  # Default sort by date
    order = request.args.get("order", "asc")  # Default order ascending

    now = datetime.now()

    featured_events = Event.query.filter_by(featured=True).order_by(Event.date.asc()).all()
    
    if sort_by == "date":
        if order == "asc":
            upcoming_events = Event.query.filter(Event.date >= now).order_by(Event.date.asc()).all()
            past_events = Event.query.filter(Event.date < now).order_by(Event.date.asc()).all()
        else:
            upcoming_events = Event.query.filter(Event.date >= now).order_by(Event.date.desc()).all()
            past_events = Event.query.filter(Event.date < now).order_by(Event.date.desc()).all()

    return render_template("events.html", upcoming_events=upcoming_events, past_events=past_events, featured_events=featured_events)

# Event detail page
@app.route("/event/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_detail.html", event=event)

# Create a new event
@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    categories = Category.query.all()  # Fetch all categories
    if request.method == "POST":
        event_date_raw = datetime.strptime(request.form.get("date"), "%d-%m-%Y %H:%M")
        
        # Determine if the event should be marked as featured
        featured = request.form.get("featured") == "1"  # Check if the checkbox was checked

        # Handle file upload for event image
        event_image = request.files.get("image")
        image_path = None
        if event_image:
            image_path = os.path.join('static/images', event_image.filename)
            event_image.save(image_path)

        event = Event(
            title=request.form.get("title"),
            description=request.form.get("description"),
            date=event_date_raw,  # Keep as datetime object
            location=request.form.get("location"),
            category_id=request.form.get("category_id"),
            featured=featured,  # Store featured status
            image=image_path  # Save image path to the database
        )
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_event.html", categories=categories)

# Edit an existing event
@app.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    categories = Category.query.all()  # Fetch categories for the dropdown
    if request.method == "POST":
        event_date_raw = datetime.strptime(request.form.get("date"), "%d-%m-%Y %H:%M")
        
        # Update the featured status
        event.featured = request.form.get("featured") == "1"  # Check if the checkbox was checked
        
        event.title = request.form.get("title")
        event.description = request.form.get("description")
        event.date = event_date_raw  # Use the converted datetime object
        event.location = request.form.get("location")
        event.category_id = request.form.get("category_id")  # Update category

        # Handle file upload for event image
        event_image = request.files.get("image")
        if event_image:
            image_path = os.path.join('static/images', event_image.filename)
            event_image.save(image_path)
            event.image = image_path  # Update the image path

        db.session.commit()
        return redirect(url_for("home"))
    
    # Format the date for rendering in the form as 'dd-mm-yyyyTHH:MM'
    formatted_date = event.date.strftime('%d-%m-%Y %H:%M')
    return render_template("edit_event.html", event=event, categories=categories, formatted_date=formatted_date)

# Delete an event
@app.route("/delete_event/<int:event_id>")
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for("home"))

# Create a new category and display existing categories
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    categories = Category.query.all()  # Fetch all categories to display

    if request.method == "POST":
        category_name = request.form.get("name").strip()  # Get and trim the category name
        
        # Check if the category name already exists
        existing_category = Category.query.filter_by(name=category_name).first()
        
        if existing_category:
            # If the category already exists, flash a message to the user
            flash(f'Category "{category_name}" already exists.', 'error')
            return redirect(url_for("add_category"))

        if category_name:
            # Only add the category if it's not empty and doesn't already exist
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash(f'Category "{category_name}" added successfully!', 'success')
            return redirect(url_for("home"))  # Redirect to home after adding the category

    return render_template("add_category.html", categories=categories)

# Search for events by title or description
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search_term").strip()  # Strip any extra spaces
        search_query = f"%{search_term}%"

        # Filter events by title or description that match the search term
        matched_events = Event.query.filter(
            (Event.title.ilike(search_query)) | 
            (Event.description.ilike(search_query))
        ).all()

        # Get the current date and time
        now = datetime.now()

        # Separate the matched events into upcoming and past
        upcoming_events = [event for event in matched_events if event.date >= now]
        past_events = [event for event in matched_events if event.date < now]

        # Render the events page with the filtered results
        return render_template("events.html", upcoming_events=upcoming_events, past_events=past_events)

    return redirect(url_for("home"))
