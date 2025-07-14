import logging

# Basic config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

# Create and export a logger instance
logger = logging.getLogger("task_manager")
