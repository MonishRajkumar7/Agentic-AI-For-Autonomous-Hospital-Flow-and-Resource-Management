import os

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

from database import (
    initialize_database,
    get_resources,
    get_patients,
)


# ============================================================
# MCP SERVER CONFIGURATION
# ============================================================

mcp = FastMCP(
    "HospitalFlowTools",
    json_response=True,

    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=[
            "hospital-flow-mcp.onrender.com",
            "hospital-flow-mcp.onrender.com:*",
            "localhost:*",
            "127.0.0.1:*",
        ],
    ),
)


# ============================================================
# TOOL 1: HOSPITAL RESOURCES
# ============================================================

@mcp.tool()
def get_hospital_resources() -> list[dict]:
    """Return the simulated hospital resource inventory."""

    initialize_database()

    return get_resources()


# ============================================================
# TOOL 2: PATIENT QUEUE
# ============================================================

@mcp.tool()
def get_patient_queue() -> list[dict]:
    """Return the simulated hospital patient queue."""

    initialize_database()

    return get_patients()


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":

    print("Starting Hospital Flow MCP Server...")

    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(
        os.environ.get("PORT", 8000)
    )

    mcp.run(
        transport="streamable-http"
    )