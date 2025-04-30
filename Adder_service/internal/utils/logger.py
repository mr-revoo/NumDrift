import logging
import os

def setup_logger(filename='app.log'):
    """
    Configure a basic logger with console and file output.
    
    Args:
        filename (str): Name of the log file (default: 'app.log'). 
                       The file will be created in numdrift/Adder_service/internal/logs.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Get the directory of the current file (logging_config.py)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Define the log directory relative to the project root
    log_dir = os.path.join(project_root, 'Adder_service', 'internal', 'logs')
    
    # Create the log directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Construct the full path for the log file
    log_file = os.path.join(log_dir, filename)
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Output to console
            logging.FileHandler(log_file)  # Save to a file
        ]
    )
    
    # Return the root logger
    logger = logging.getLogger()
    logger.debug(f"Logger configured with log file {log_file}")
    return logger