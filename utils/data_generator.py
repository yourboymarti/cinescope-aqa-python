import uuid


def generate_user_data() -> dict:
    short_id = uuid.uuid4().hex[:8]
    password = "12345678Aa"

    return {
        "email": f"test_{short_id}@mail.com",
        "fullName": "Test User",
        "password": password,
        "passwordRepeat": password,
        "roles": ["ADMIN"],
    }