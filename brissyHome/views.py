from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .forms import LoginForm, RegisterForm, BookmarkForm, EnquiryForm, OfferForm, PropertyForm
from .wrappers import login_required, buyer_required, seller_required, admin_required
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("main", __name__)

@bp.route('/')
@bp.route('/listings/')
def index():
    filters = {
        'search': request.args.get('search', '').strip(),
        'category_id': request.args.get('category_id') or None,
        'property_type': request.args.get('property_type') or None,
        'bedrooms': request.args.get('bedrooms') or None,
        'min_price': request.args.get('min_price') or None,
        'max_price': request.args.get('max_price') or None,
        'solar': request.args.get('solar') or None,
    }
    properties = db.get_properties(filters)
    categories = db.get_categories()
    property_types = db.get_property_types()

    return render_template(
        'index.html',
        properties=properties,
        categories=categories,
        property_types=property_types,
        filters=filters
    )

@bp.route('/property/<int:property_id>/')
def property_details(property_id):
    property_row = db.get_property(property_id)

    if not property_row:
        return render_template(
            'error.html',
            error_code=404,
            error_title='Property Not Found',
            error_message='The requested property could not be found.'
        ), 404

    documents = db.get_property_documents(property_id)

    bookmarked = False
    if 'user' in session:
        bookmarked = db.is_bookmarked(session['user']['user_id'], property_id)

    return render_template(
        'property_details.html',
        property=property_row,
        documents=documents,
        bookmarked=bookmarked,
        bookmark_form=BookmarkForm(),
        enquiry_form=EnquiryForm(),
        offer_form=OfferForm()
    )

@bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        db.add_user(
            form.username.data,
            form.email.data,
            form.password.data,
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

@bp.post('/property/<int:property_id>/bookmark/')
@buyer_required
def save_property(property_id):
    form = BookmarkForm()

    if form.validate_on_submit():
        db.add_bookmark(session['user']['user_id'], property_id, form.notes.data)
        flash('Property saved to your bookmarks.')
    else:
        flash('Bookmark could not be saved.', 'error')

    return redirect(url_for('main.property_details', property_id=property_id))

@bp.post('/property/<int:property_id>/enquiry/')
@buyer_required
def submit_enquiry(property_id):
    form = EnquiryForm()

    if form.validate_on_submit():
        db.add_enquiry(session['user']['user_id'], property_id, form.message.data)
        flash('Your enquiry has been sent to the agent.')

    return redirect(url_for('main.property_details', property_id=property_id))

@bp.route('/manage/enquiries/')
@seller_required
def manage_enquiries():
    enquiries = db.get_manage_enquiries(session['user'])
    return render_template('manage_enquiries.html', enquiries=enquiries)

@bp.route('/admin/users/')
@admin_required
def admin_users():
    users = db.get_users()
    return render_template('admin_users.html', users=users)


@bp.route('/manage/listings/new/', methods=['GET', 'POST'])
@seller_required
def new_listing():
    form = PropertyForm()
    _set_property_form_choices(form)

    if form.validate_on_submit():
        image_filename = _save_uploaded_image(form.image_file.data) or 'property1.jpg'
        property_id = db.create_property(
            _property_form_data(form),
            session['user']['user_id'],
            image_filename
        )

        flash('Listing created successfully.')
        return redirect(url_for('main.property_details', property_id=property_id))

    return render_template('listing_form.html', form=form, title='Create New Listing')