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

def get_property_types():
    return _fetchall(
        """
        SELECT DISTINCT property_type 
        FROM properties 
        ORDER BY property_type
        """
    )


def get_properties(filters=None):
    filters = filters or {}

    query = """
        SELECT p.*,
               CONCAT(u.first_name, ' ', u.last_name) AS seller_name
        FROM properties p
        JOIN users u ON p.seller_id = u.user_id
        WHERE 1 = 1
    """

    params = []

    search = filters.get("search")
    if search:
        query += """
            AND (
                p.title LIKE %s 
                OR p.description LIKE %s 
                OR p.address LIKE %s
                OR p.suburb LIKE %s 
                OR p.postcode LIKE %s
            )
        """
        like = f"%{search}%"
        params.extend([like, like, like, like, like])

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
        SELECT p.*,
               CONCAT(u.first_name, ' ', u.last_name) AS seller_name,
               u.email AS seller_email,
               u.phone AS seller_phone
        FROM properties p
        JOIN users u ON p.seller_id = u.user_id
        WHERE p.property_id = %s
        """,
        (property_id,),
    )


def create_property(data, seller_id, image_filename):
    return _execute(
        """
        INSERT INTO properties
        (
            seller_id,
            title,
            description,
            address,
            suburb,
            postcode,
            property_type,
            rent_per_week,
            bedrooms,
            bathrooms,
            solar_available,
            pet_friendly,
            image_filename
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            seller_id,
            data["title"],
            data["description"],
            data["address"],
            data["suburb"],
            data["postcode"],
            data["property_type"],
            data["rent_per_week"],
            data["bedrooms"],
            data["bathrooms"],
            data["solar_available"],
            data["pet_friendly"],
            image_filename,
        ),
    )


def update_property(property_id, data, image_filename):
    return _execute(
        """
        UPDATE properties SET
            title = %s,
            description = %s,
            address = %s,
            suburb = %s,
            postcode = %s,
            property_type = %s,
            rent_per_week = %s,
            bedrooms = %s,
            bathrooms = %s,
            solar_available = %s,
            pet_friendly = %s,
            image_filename = %s
        WHERE property_id = %s
        """,
        (
            data["title"],
            data["description"],
            data["address"],
            data["suburb"],
            data["postcode"],
            data["property_type"],
            data["rent_per_week"],
            data["bedrooms"],
            data["bathrooms"],
            data["solar_available"],
            data["pet_friendly"],
            image_filename,
            property_id,
        ),
    )


def delete_property(property_id):
    return _execute(
        "DELETE FROM properties WHERE property_id = %s",
        (property_id,),
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


def get_manage_properties(user):
    if user["role"] == "admin":
        return get_properties()

    return _fetchall(
        """
        SELECT p.*,
               CONCAT(u.first_name, ' ', u.last_name) AS seller_name
        FROM properties p
        JOIN users u ON p.seller_id = u.user_id
        WHERE p.seller_id = %s
        ORDER BY p.created_at DESC, p.property_id DESC
        """,
        (user["user_id"],),
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


def get_user_by_username_or_email(identifier):
    return _fetchone(
        """
        SELECT *
        FROM users
        WHERE username = %s OR email = %s
        """,
        (identifier, identifier),
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
        """
        DELETE FROM users 
        WHERE user_id = %s AND role <> 'admin'
        """,
        (user_id,),
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
        SELECT b.bookmark_id,
               b.notes,
               b.created_at AS bookmarked_at,
               p.*
        FROM bookmarks b
        JOIN properties p ON b.property_id = p.property_id
        WHERE b.user_id = %s
        ORDER BY b.created_at DESC
        """,
        (user_id,),
    )

def update_property(property_id, data, image_filename):
    return _execute(
        """
        UPDATE properties SET
            title = %s,
            description = %s,
            address = %s,
            suburb = %s,
            postcode = %s,
            property_type = %s,
            rent_per_week = %s,
            bedrooms = %s,
            bathrooms = %s,
            solar_available = %s,
            pet_friendly = %s,
            image_filename = %s
        WHERE property_id = %s
        """,
        (
            data["title"],
            data["description"],
            data["address"],
            data["suburb"],
            data["postcode"],
            data["property_type"],
            data["rent_per_week"],
            data["bedrooms"],
            data["bathrooms"],
            data["solar_available"],
            data["pet_friendly"],
            image_filename,
            property_id,
        ),
    )

def delete_property(property_id):
    _execute(
        "DELETE FROM bookmarks WHERE property_id = %s",
        (property_id,),
    )
    return _execute(
        "DELETE FROM properties WHERE property_id = %s",
        (property_id,),
    )