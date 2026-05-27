from . import mysql


def _fetchall(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close()
    return rows


def _fetchone(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    row = cur.fetchone()
    cur.close()
    return row


def _execute(query, params=None):
    cur = mysql.connection.cursor()
    cur.execute(query, params or ())
    mysql.connection.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id


def get_categories():
    return _fetchall(
        "SELECT category_id, category_name FROM categories ORDER BY category_name"
    )


def get_property_types():
    return _fetchall(
        "SELECT DISTINCT property_type FROM properties ORDER BY property_type"
    )


def get_properties(filters=None):
    filters = filters or {}

    query = """
        SELECT p.*, c.category_name,
               CONCAT(u.first_name, ' ', u.last_name) AS seller_name
        FROM properties p
        JOIN categories c ON p.category_id = c.category_id
        JOIN users u ON p.seller_id = u.user_id
        WHERE 1 = 1
    """

    params = []

    search = filters.get("search")
    if search:
        query += """
            AND (
                p.title LIKE %s OR p.description LIKE %s OR p.address LIKE %s
                OR p.suburb LIKE %s OR p.postcode LIKE %s
            )
        """
        like = f"%{search}%"
        params.extend([like, like, like, like, like])

    if filters.get("category_id"):
        query += " AND p.category_id = %s"
        params.append(filters["category_id"])

    if filters.get("property_type"):
        query += " AND p.property_type = %s"
        params.append(filters["property_type"])

    if filters.get("bedrooms"):
        if str(filters["bedrooms"]) == "4":
            query += " AND p.bedrooms >= 4"
        else:
            query += " AND p.bedrooms = %s"
            params.append(filters["bedrooms"])

    if filters.get("min_price"):
        query += " AND p.rent_per_week >= %s"
        params.append(filters["min_price"])

    if filters.get("max_price"):
        query += " AND p.rent_per_week <= %s"
        params.append(filters["max_price"])

    if filters.get("solar") == "yes":
        query += " AND p.solar_available = TRUE"
    elif filters.get("solar") == "no":
        query += " AND p.solar_available = FALSE"

    query += " ORDER BY p.created_at DESC, p.property_id DESC"

    return _fetchall(query, tuple(params))


def get_property(property_id):
    return _fetchone(
        """
        SELECT p.*, c.category_name,
               CONCAT(u.first_name, ' ', u.last_name) AS seller_name,
               u.email AS seller_email,
               u.phone AS seller_phone
        FROM properties p
        JOIN categories c ON p.category_id = c.category_id
        JOIN users u ON p.seller_id = u.user_id
        WHERE p.property_id = %s
        """,
        (property_id,),
    )


def get_property_documents(property_id):
    return _fetchall(
        """
        SELECT document_id, document_name, document_url
        FROM property_documents
        WHERE property_id = %s
        ORDER BY document_name
        """,
        (property_id,),
    )


def get_user_by_username(username):
    return _fetchone(
        "SELECT * FROM users WHERE username = %s",
        (username,),
    )


def get_user_by_email(email):
    return _fetchone(
        "SELECT * FROM users WHERE email = %s",
        (email,),
    )


def get_users():
    return _fetchall(
        """
        SELECT user_id, username, email, first_name, last_name, phone, role, created_at
        FROM users
        ORDER BY role, username
        """
    )


def add_user(username, email, password_hash, first_name, last_name, phone, role):
    return _execute(
        """
        INSERT INTO users 
        (username, email, password_hash, first_name, last_name, phone, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (username, email, password_hash, first_name, last_name, phone, role),
    )


def delete_user(user_id):
    return _execute(
        "DELETE FROM users WHERE user_id = %s AND role <> %s",
        (user_id, "admin"),
    )


def get_manage_properties(user):
    if user["role"] == "admin":
        return get_properties()

    return _fetchall(
        """
        SELECT p.*, c.category_name,
               CONCAT(u.first_name, ' ', u.last_name) AS seller_name
        FROM properties p
        JOIN categories c ON p.category_id = c.category_id
        JOIN users u ON p.seller_id = u.user_id
        WHERE p.seller_id = %s
        ORDER BY p.created_at DESC
        """,
        (user["user_id"],),
    )


def can_manage_property(user, property_id):
    if user["role"] == "admin":
        return True

    row = _fetchone(
        """
        SELECT property_id 
        FROM properties 
        WHERE property_id = %s AND seller_id = %s
        """,
        (property_id, user["user_id"]),
    )

    return row is not None


def create_property(data, seller_id, image_filename):
    return _execute(
        """
        INSERT INTO properties
        (
            seller_id, category_id, title, description, address, suburb, postcode,
            property_type, rent_per_week, bond_amount, bedrooms, bathrooms,
            car_spaces, size_sqm, solar_available, pet_friendly,
            availability_status, image_filename, document_url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            seller_id,
            data["category_id"],
            data["title"],
            data["description"],
            data["address"],
            data["suburb"],
            data["postcode"],
            data["property_type"],
            data["rent_per_week"],
            data["bond_amount"],
            data["bedrooms"],
            data["bathrooms"],
            data["car_spaces"],
            data.get("size_sqm"),
            data["solar_available"],
            data["pet_friendly"],
            data["availability_status"],
            image_filename,
            data.get("document_url"),
        ),
    )


def update_property(property_id, data, image_filename):
    return _execute(
        """
        UPDATE properties SET
            category_id = %s,
            title = %s,
            description = %s,
            address = %s,
            suburb = %s,
            postcode = %s,
            property_type = %s,
            rent_per_week = %s,
            bond_amount = %s,
            bedrooms = %s,
            bathrooms = %s,
            car_spaces = %s,
            size_sqm = %s,
            solar_available = %s,
            pet_friendly = %s,
            availability_status = %s,
            image_filename = %s,
            document_url = %s
        WHERE property_id = %s
        """,
        (
            data["category_id"],
            data["title"],
            data["description"],
            data["address"],
            data["suburb"],
            data["postcode"],
            data["property_type"],
            data["rent_per_week"],
            data["bond_amount"],
            data["bedrooms"],
            data["bathrooms"],
            data["car_spaces"],
            data.get("size_sqm"),
            data["solar_available"],
            data["pet_friendly"],
            data["availability_status"],
            image_filename,
            data.get("document_url"),
            property_id,
        ),
    )


def delete_property(property_id):
    return _execute(
        "DELETE FROM properties WHERE property_id = %s",
        (property_id,),
    )


def is_bookmarked(user_id, property_id):
    row = _fetchone(
        """
        SELECT bookmark_id 
        FROM bookmarks 
        WHERE user_id = %s AND property_id = %s
        """,
        (user_id, property_id),
    )

    return row is not None


def add_bookmark(user_id, property_id, notes):
    return _execute(
        """
        INSERT INTO bookmarks (user_id, property_id, notes)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            notes = VALUES(notes),
            created_at = CURRENT_TIMESTAMP
        """,
        (user_id, property_id, notes),
    )


def remove_bookmark(user_id, property_id):
    return _execute(
        """
        DELETE FROM bookmarks 
        WHERE user_id = %s AND property_id = %s
        """,
        (user_id, property_id),
    )


def get_saved_properties(user_id):
    return _fetchall(
        """
        SELECT b.bookmark_id, b.notes, b.created_at AS bookmarked_at,
               p.*, c.category_name
        FROM bookmarks b
        JOIN properties p ON b.property_id = p.property_id
        JOIN categories c ON p.category_id = c.category_id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
        """,
        (user_id,),
    )


def add_enquiry(user_id, property_id, message):
    return _execute(
        """
        INSERT INTO enquiries (user_id, property_id, message, status)
        VALUES (%s, %s, %s, 'new')
        """,
        (user_id, property_id, message),
    )


def add_offer(user_id, property_id, offer_amount, message):
    return _execute(
        """
        INSERT INTO offers (user_id, property_id, offer_amount, message, status)
        VALUES (%s, %s, %s, %s, 'pending')
        """,
        (user_id, property_id, offer_amount, message),
    )


def get_enquiries_for_user(user):
    query = """
        SELECT e.*, p.title, p.suburb, p.seller_id,
               CONCAT(u.first_name, ' ', u.last_name) AS buyer_name,
               u.email AS buyer_email
        FROM enquiries e
        JOIN properties p ON e.property_id = p.property_id
        JOIN users u ON e.user_id = u.user_id
    """

    params = []

    if user["role"] != "admin":
        query += " WHERE p.seller_id = %s"
        params.append(user["user_id"])

    query += " ORDER BY e.created_at DESC"

    return _fetchall(query, tuple(params))


def get_offers_for_user(user):
    query = """
        SELECT o.*, p.title, p.suburb, p.seller_id,
               CONCAT(u.first_name, ' ', u.last_name) AS buyer_name,
               u.email AS buyer_email
        FROM offers o
        JOIN properties p ON o.property_id = p.property_id
        JOIN users u ON o.user_id = u.user_id
    """

    params = []

    if user["role"] != "admin":
        query += " WHERE p.seller_id = %s"
        params.append(user["user_id"])

    query += " ORDER BY o.created_at DESC"

    return _fetchall(query, tuple(params))


def update_enquiry_status(enquiry_id, status, user):
    if user["role"] == "admin":
        return _execute(
            "UPDATE enquiries SET status = %s WHERE enquiry_id = %s",
            (status, enquiry_id),
        )

    return _execute(
        """
        UPDATE enquiries e
        JOIN properties p ON e.property_id = p.property_id
        SET e.status = %s
        WHERE e.enquiry_id = %s AND p.seller_id = %s
        """,
        (status, enquiry_id, user["user_id"]),
    )


def update_offer_status(offer_id, status, user):
    if user["role"] == "admin":
        return _execute(
            "UPDATE offers SET status = %s WHERE offer_id = %s",
            (status, offer_id),
        )

    return _execute(
        """
        UPDATE offers o
        JOIN properties p ON o.property_id = p.property_id
        SET o.status = %s
        WHERE o.offer_id = %s AND p.seller_id = %s
        """,
        (status, offer_id, user["user_id"]),
    )