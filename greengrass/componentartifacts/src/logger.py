import logging
import os

log = logging.getLogger("PQI_lookout_demo")

# Use same levelset as connected_brewery package
log_level = "DEBUG" if os.getenv("LOCAL") else "INFO"
log.setLevel(log_level)

# Add formatter with time, name, levelname, function name and message
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
if not log.handlers:
    log.addHandler(ch)