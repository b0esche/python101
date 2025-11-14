import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional, Dict, Any
import json

class LoggerSetup:
    @staticmethod
    def setup_basic_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    @staticmethod
    def setup_file_logger(name: str = "app", 
                          log_file: str = "app.log",
                          level: int = logging.INFO,
                          max_bytes: int = 10*1024*1024,
                          backup_count: int = 5) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count
            )
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def setup_json_logger(name: str = "app",
                         log_file: str = "app.json",
                         level: int = logging.INFO) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            class JSONFormatter(logging.Formatter):
                def format(self, record):
                    log_entry = {
                        'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                        'level': record.levelname,
                        'logger': record.name,
                        'message': record.getMessage(),
                        'module': record.module,
                        'function': record.funcName,
                        'line': record.lineno
                    }
                    
                    if record.exc_info:
                        log_entry['exception'] = self.formatException(record.exc_info)
                    
                    return json.dumps(log_entry)
            
            file_handler = logging.FileHandler(log_file)
            json_formatter = JSONFormatter()
            file_handler.setFormatter(json_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def setup_timed_logger(name: str = "app",
                          log_file: str = "app.log",
                          when: str = 'midnight',
                          interval: int = 1,
                          backup_count: int = 7) -> logging.Logger:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            timed_handler = logging.handlers.TimedRotatingFileHandler(
                log_file, when=when, interval=interval, backupCount=backup_count
            )
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            timed_handler.setFormatter(formatter)
            logger.addHandler(timed_handler)
        
        return logger

class CustomLogger:
    def __init__(self, name: str = "custom"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        error_handler = logging.FileHandler('errors.log')
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs):
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        self.logger.critical(message, extra=kwargs)
    
    def exception(self, message: str, **kwargs):
        self.logger.exception(message, extra=kwargs)

class ContextLogger:
    def __init__(self, logger: logging.Logger, context: Dict[str, Any]):
        self.logger = logger
        self.context = context
    
    def _log_with_context(self, level: int, message: str, **kwargs):
        extra = {'context': {**self.context, **kwargs}}
        self.logger.log(level, message, extra=extra)
    
    def debug(self, message: str, **kwargs):
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log_with_context(logging.CRITICAL, message, **kwargs)

def demo_basic_logging():
    print("1. Basic Logging Example")
    print("-" * 30)
    
    logger = LoggerSetup.setup_basic_logger("demo", logging.DEBUG)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

def demo_file_logging():
    print("\n2. File Logging Example")
    print("-" * 30)
    
    logger = LoggerSetup.setup_file_logger("file_demo", "demo.log", logging.DEBUG)
    
    logger.info("Starting file logging demo")
    logger.debug("Debug information")
    logger.warning("Warning: something might be wrong")
    logger.error("Error: something went wrong")
    
    print("Check 'demo.log' file for logged messages")

def demo_json_logging():
    print("\n3. JSON Logging Example")
    print("-" * 30)
    
    logger = LoggerSetup.setup_json_logger("json_demo", "demo.json", logging.DEBUG)
    
    logger.info("Starting JSON logging demo")
    logger.warning("Warning in JSON format")
    logger.error("Error in JSON format")
    
    print("Check 'demo.json' file for JSON formatted logs")

def demo_custom_logging():
    print("\n4. Custom Logging Example")
    print("-" * 30)
    
    custom_logger = CustomLogger("custom_demo")
    
    custom_logger.info("This uses custom logger")
    custom_logger.warning("Custom warning message")
    custom_logger.error("Custom error message")
    
    print("Check 'errors.log' file for error messages")

def demo_context_logging():
    print("\n5. Context Logging Example")
    print("-" * 30)
    
    base_logger = LoggerSetup.setup_basic_logger("context_demo", logging.INFO)
    
    context_logger = ContextLogger(base_logger, {
        'user_id': '12345',
        'session_id': 'abcde-12345',
        'request_id': 'req-67890'
    })
    
    context_logger.info("User logged in")
    context_logger.warning("Invalid input detected", input_field="email")
    context_logger.error("Database connection failed", database="users_db")

def demo_exception_logging():
    print("\n6. Exception Logging Example")
    print("-" * 30)
    
    logger = LoggerSetup.setup_file_logger("exception_demo", "exceptions.log", logging.DEBUG)
    
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.exception("Division by zero error occurred")
    
    try:
        data = {"key": "value"}
        value = data["nonexistent_key"]
    except KeyError as e:
        logger.exception("Key error occurred")
    
    print("Check 'exceptions.log' file for exception details")

def demo_performance_logging():
    import time
    
    print("\n7. Performance Logging Example")
    print("-" * 30)
    
    logger = LoggerSetup.setup_basic_logger("performance_demo", logging.INFO)
    
    start_time = time.time()
    
    logger.info("Starting performance test")
    
    for i in range(1000):
        result = i * i
    
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"Performance test completed", extra={
        'operation': 'square_calculation',
        'iterations': 1000,
        'duration_seconds': duration,
        'iterations_per_second': 1000 / duration
    })

def configure_logging_from_dict():
    print("\n8. Dictionary Configuration Example")
    print("-" * 30)
    
    try:
        import logging.config as logging_config
        
        config = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
                },
                'detailed': {
                    'format': '%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'standard'
                },
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.FileHandler',
                    'filename': 'dict_config.log',
                    'formatter': 'detailed'
                }
            },
            'loggers': {
                'dict_demo': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': False
                }
            }
        }
        
        logging_config.dictConfig(config)
        
        logger = logging.getLogger('dict_demo')
        logger.debug("Debug message from dict config")
        logger.info("Info message from dict config")
        logger.warning("Warning message from dict config")
        
        print("Check 'dict_config.log' file for dict config logs")
        
    except ImportError:
        print("logging.config not available in this Python version")

def main():
    print("Logging Configuration Examples")
    print("=" * 50)
    
    demo_basic_logging()
    demo_file_logging()
    demo_json_logging()
    demo_custom_logging()
    demo_context_logging()
    demo_exception_logging()
    demo_performance_logging()
    
    configure_logging_from_dict()
    
    print("\nLogging examples completed!")
    print("\nGenerated log files:")
    for file in ['demo.log', 'demo.json', 'errors.log', 'exceptions.log', 'dict_config.log']:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  {file}: {size} bytes")

if __name__ == "__main__":
    main()