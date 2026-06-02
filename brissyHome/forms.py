from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import *
from wtforms.validators import *

class LoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(max=50)]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired()]
    )
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=3, max=50)]
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=120)]
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=80)]
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=80)]
    )
    phone = StringField(
        "Phone",
        validators=[InputRequired(), Length(min=8, max=20)]
    )
    role = SelectField(
        "Account Type",
        choices=[
            ("buyer", "Buyer/Tenant"),
            ("seller", "Seller/Agent"),
        ],
        validators=[InputRequired()]
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            InputRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )
    submit = SubmitField("Register")


class BookmarkForm(FlaskForm):
    notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField("Save Property")


class PropertyForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=150)]
    )
    description = TextAreaField(
        "Description",
        validators=[InputRequired(), Length(min=20, max=3000)]
    )
    address = StringField(
        "Address",
        validators=[InputRequired(), Length(max=200)]
    )
    suburb = StringField(
        "Suburb",
        validators=[InputRequired(), Length(max=100)]
    )
    postcode = StringField(
        "Postcode",
        validators=[InputRequired(), Length(min=4, max=4)]
    )
    property_type = SelectField(
        "Property Type",
        choices=[
            ("House", "House"),
            ("Apartment", "Apartment"),
            ("Unit", "Unit"),
            ("Townhouse", "Townhouse"),
            ("Studio", "Studio"),
            ("Room", "Room"),
        ],
        validators=[InputRequired()]
    )
    rent_per_week = DecimalField(
        "Rent Per Week",
        validators=[InputRequired(), NumberRange(min=1)]
    )
    bedrooms = IntegerField(
        "Bedrooms",
        validators=[InputRequired(), NumberRange(min=0, max=20)]
    )
    bathrooms = IntegerField(
        "Bathrooms",
        validators=[InputRequired(), NumberRange(min=0, max=20)]
    )
    solar_available = BooleanField("Solar Available")
    pet_friendly = BooleanField("Pet Friendly")
    image_file = FileField(
        "Property Image",
        validators=[
            Optional(),
            FileAllowed(["jpg", "jpeg", "png", "webp"], "Images only.")
        ]
    )
    submit = SubmitField("Save Listing")