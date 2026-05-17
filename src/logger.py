import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    # Centralized logger for tracing and debugging across the system
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Format: [Time] [Level] [Module] - Message
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - [%(name)s] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler for tracing (can be routed to a file in production)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

# Initialize a global system logger
sys_logger = setup_logger("AgentOS")