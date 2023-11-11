import os

PORT: int = int(os.environ.get("NOTIF_PORT", 1339))
ADMIN_PSWD: str = os.environ.get("ADMIN_NOTIF_PSWD")
NOTIF_PSWD: str = os.environ.get("NOTIF_PSWD")
