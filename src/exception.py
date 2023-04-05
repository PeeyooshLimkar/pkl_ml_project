import sys
from src.logger import logging



# error : own
def error_message_detail(error, error_detail:sys):

    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = '''Error in Python Script.
    1. File Name :- {0} 
    2. Line No. :- {1}
    3. Error Message :- {2}'''.format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


# error_message : own
class Custom_Exception(Exception):

    def __init__(self, error_msg, error_info:sys):
        super().__init__(error_msg)
        self.error_msg = error_message_detail(error = error_msg,
                                              error_detail = error_info)

    def __str__(self):
        return self.error_msg
    

# # TO CHEKE WORKING OR NOT
# if __name__ == '__main__':
#     try:
#         temp = 123/0
#     except Exception as e:
#         logging.info('Divide By Zerro Error')
#         raise Custom_Exception(e, sys)

