"""Environment-configured authentication for Hospital Flow AI."""

import hmac
import os
import streamlit as st

from dotenv import load_dotenv

load_dotenv()


# ============================================================
# CONFIGURATION LOADER
# ============================================================

def get_setting(name, default=""):
    """Read from Streamlit Cloud Secrets or local .env."""

    # First check local environment variables.
    value = os.getenv(name)

    if value:
        return value

    # Then check Streamlit Cloud Secrets.
    try:
        value = st.secrets.get(name, default)
        return value or default
    except Exception:
        return default


# ============================================================
# ROLE-BASED LOGIN ACCOUNTS
# ============================================================

ROLE_ACCOUNTS = {

    "Admin": {
        "username": get_setting("HF_ADMIN_USERNAME"),
        "password": get_setting("HF_ADMIN_PASSWORD"),
    },

    "Hospital Operations Manager": {
        "username": get_setting("HF_MANAGER_USERNAME"),
        "password": get_setting("HF_MANAGER_PASSWORD"),
    },

    "Clinical Staff": {
        "username": get_setting("HF_CLINICAL_USERNAME"),
        "password": get_setting("HF_CLINICAL_PASSWORD"),
    },

}


# ============================================================
# ROLE-BASED PAGE ACCESS
# ============================================================

ROLE_PAGES = {

    "Admin": [
        "Dashboard",
        "Register Patient",
        "Patient Queue",
        "Resource Management",
        "Bed Allocation",
        "Department Routing",
        "Discharge & Transfers",
        "Notifications",
        "Agent Workflow",
        "About Project",
    ],

    "Hospital Operations Manager": [
        "Dashboard",
        "Register Patient",
        "Patient Queue",
        "Resource Management",
        "Bed Allocation",
        "Department Routing",
        "Discharge & Transfers",
        "Notifications",
        "Agent Workflow",
        "About Project",
    ],

    "Clinical Staff": [
        "Dashboard",
        "Register Patient",
        "Patient Queue",
        "Bed Allocation",
        "Department Routing",
        "Discharge & Transfers",
        "About Project",
    ],

}


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate(username: str, password: str):

    """Return the matched role or None."""

    username = username.strip()

    for role, credentials in ROLE_ACCOUNTS.items():

        configured_user = credentials["username"]
        configured_password = credentials["password"]

        if not configured_user or not configured_password:
            continue

        if (
            hmac.compare_digest(username, configured_user)
            and hmac.compare_digest(password, configured_password)
        ):
            return role

    return None


# ============================================================
# CHECK CONFIGURATION
# ============================================================

def has_configured_accounts() -> bool:

    return all(
        account["username"] and account["password"]
        for account in ROLE_ACCOUNTS.values()
    )