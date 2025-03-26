import sys
import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

class NetworkSecurityException(Exception):
    def __init__(self, error_message):
        self.error_message = error_message
        # Capture the exception traceback info using sys.exc_info()
        _, _, exc_tb = sys.exc_info()
        
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = 'unknown'
            self.file_name = 'unknown'
    
    def __str__(self):
        return "Error occurred in python script name [{}] line number [{}] error message [{}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )
    
if __name__ == '__main__':
    try:
        logging.info("Enter the try block")
        a = 1 / 0  # This will cause a ZeroDivisionError
        print("This will not be printed", a)
    except Exception as e:
        # Remove the extra sys argument
        raise NetworkSecurityException(e)


