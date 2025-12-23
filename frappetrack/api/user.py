import frappe
from frappetrack.utils.auth_utils import get_logged_in_user


@frappe.whitelist(allow_guest=True)
def get_profile():
    """
    Endpoint to get user's / employee profile details.
    """
    try:
        auth = frappe.get_request_header("Authorization")

        if not auth or not auth.startswith("Bearer "):
            frappe.throw("Missing token")

        token = auth.split(" ")[1]

    # Example: token stored as api_key
        user = frappe.db.get_value(
            "User",
            {"api_key": token},
            ["name", "full_name", "email", "user_type"],
            as_dict=True
        )

        if not user:
            frappe.throw("Invalid token")

        return {
            "success": True,
            "user": user
        }

    except Exception:
        return {
            "success": False,
            "message": "Unable to fetch profile"
        }
