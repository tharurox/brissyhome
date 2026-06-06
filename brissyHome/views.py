from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .forms import LoginForm, RegisterForm, BookmarkForm, PropertyForm
from .wrappers import login_required, buyer_required, seller_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import *
from flask import current_app

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
 
    filters = {}
    properties = db.get_properties(filters)

    return render_template(
        "index.html",
        properties=properties[:3]   
    )

@bp.route("/listings/")
def listings():
    filters = {
        'search': request.args.get('search', '').strip(),
        'property_type': request.args.get('property_type') or None,
        'bedrooms': request.args.get('bedrooms') or None,
        'min_price': request.args.get('min_price') or None,
        'max_price': request.args.get('max_price') or None,
        'solar': request.args.get('solar') or None,
    }
    properties = db.get_properties(filters)
    property_types = db.get_property_types()

    return render_template(
        'listings.html',
        properties=properties,
        property_types=property_types,
        filters=filters
    )

@bp.route('/property/<property_id>/')
def property_details(property_id):
    property_row = db.get_property(property_id)

    if not property_row:
        return render_template(
            'error.html',
            error_code=404,
            error_title='Property Not Found',
            error_message='The requested property could not be found.'
        ), 404

    bookmarked = False
    if 'user' in session:
        bookmarked = db.is_bookmarked(session['user']['user_id'], property_id)

    return render_template(
        'property_details.html',
        property=property_row,
        bookmarked=bookmarked,
        bookmark_form=BookmarkForm()
    )

@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        db.add_user(
            form.username.data,
            form.email.data,
            password_hash,
            form.first_name.data,
            form.last_name.data,
            form.phone.data,
            form.role.data
        )

        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = db.get_user_by_username(form.username.data)

        if not user or not check_password_hash(user['password_hash'], form.password.data):
            flash('Invalid username or password.', 'error')
            return render_template('login.html', form=form)

        session['user'] = {
            'user_id': user['user_id'],
            'username': user['username'],
            'first_name': user['first_name'],
            'role': user['role']
        }

        flash(f"Welcome back, {user['first_name']}!")
        return redirect(url_for('main.index'))

    return render_template('login.html', form=form)

@bp.route('/saved/')
@buyer_required
def saved_properties():
    saved = db.get_saved_properties(session['user']['user_id'])
    return render_template('saved_properties.html', saved=saved)

@bp.post('/property/<property_id>/bookmark/')
@buyer_required
def save_property(property_id):
    form = BookmarkForm()

    if form.validate_on_submit():
        db.add_bookmark(session['user']['user_id'], property_id, form.notes.data)
        flash('Property saved to your bookmarks.')
    else:
        flash('Bookmark could not be saved.', 'error')

    return redirect(url_for('main.property_details', property_id=property_id))

@bp.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))

@bp.route("/offers/")
def offers():
    return render_template('offers_page.html')

@bp.route("/manage/listings/")
@seller_required
def manage_listings():
    properties = db.get_manage_properties(session["user"])
    return render_template("manage_listings.html", properties=properties)

def _save_uploaded_image(file_storage):
    if not file_storage or not file_storage.filename:
        return None

    filename = secure_filename(file_storage.filename)
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file_storage.save(upload_path)

    return filename

def _property_form_data(form):
    return {
        "title": form.title.data,
        "description": form.description.data,
        "address": form.address.data,
        "suburb": form.suburb.data,
        "postcode": form.postcode.data,
        "property_type": form.property_type.data,   
        "rent_per_week": form.rent_per_week.data,
        "bedrooms": form.bedrooms.data,
        "bathrooms": form.bathrooms.data,
        "solar_available": form.solar_available.data,
        "pet_friendly": form.pet_friendly.data,
    }

@bp.route('/manage/listings/new/', methods=['GET', 'POST'])
@seller_required
def new_listing():
    form = PropertyForm()

    if form.validate_on_submit():
        image_filename = _save_uploaded_image(form.image_file.data)
        property_id = db.create_property(
            _property_form_data(form),
            session['user']['user_id'],
            image_filename
        )

        flash('Listing created successfully.')
        return redirect(url_for('main.property_details', property_id=property_id))

    return render_template('listing_form.html', form=form, title='Create New Listing')


@bp.post("/saved/<property_id>/remove/")
@buyer_required
def remove_saved_property(property_id):
    db.remove_bookmark(session["user"]["user_id"], property_id)
    flash("Property removed from saved properties.", "success")
    return redirect(url_for("main.saved_properties"))


@bp.route("/manage/listings/<property_id>/edit/", methods=["GET", "POST"])
@seller_required
def edit_listing(property_id):
    property_row = db.get_property(property_id)

    if not property_row:
        return render_template(
            "error.html",
            error_code=404,
            error_title="Property Not Found",
            error_message="The requested property could not be found."
        ), 404

    if not db.can_manage_property(session["user"], property_id):
        flash("You are not allowed to edit this property.", "error")
        return redirect(url_for("main.manage_listings"))

    form = PropertyForm()

    if request.method == "GET":
        form.title.data = property_row["title"]
        form.description.data = property_row["description"]
        form.address.data = property_row["address"]
        form.suburb.data = property_row["suburb"]
        form.postcode.data = property_row["postcode"]
        form.property_type.data = property_row["property_type"]
        form.rent_per_week.data = property_row["rent_per_week"]
        form.bedrooms.data = property_row["bedrooms"]
        form.bathrooms.data = property_row["bathrooms"]
        form.solar_available.data = property_row["solar_available"]
        form.pet_friendly.data = property_row["pet_friendly"]

        if hasattr(form, "availability_status") and "availability_status" in property_row:
            form.availability_status.data = property_row["availability_status"]

    if form.validate_on_submit():
        image_filename = property_row["image_filename"]

        uploaded_image = _save_uploaded_image(form.image_file.data)

        if uploaded_image:
            image_filename = uploaded_image

        db.update_property(
            property_id,
            _property_form_data(form),
            image_filename
        )

        flash("Listing updated successfully.", "success")
        return redirect(url_for("main.manage_listings"))

    return render_template(
        "listing_form.html",
        form=form,
        title="Edit Listing"
    )

@bp.post("/manage/listings/<property_id>/delete/")
@seller_required
def delete_listing(property_id):
    db.delete_property(property_id)
    flash("Listing deleted successfully.", "success")
    return redirect(url_for("main.manage_listings"))