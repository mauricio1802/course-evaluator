from .colors import *
import logging

datefmt ='%Y-%m-%d %H:%M:%S'
formatC  = f'%(color)s%(levelname)s{RESET} - {BLACKB}%(name)s{RESET} - {GREEN}%(method)s{RESET} - %(message)s'
formatF  = f'%(asctime)s - %(levelname)s - %(name)s - %(method)s - %(message)s'

def LoggerFactory(name="root", log=False):
    '''
    Create a custom #LOGGER to use colors in the logs
    '''
    if log:
        logging.basicConfig(format=formatF, datefmt=datefmt)
    else:
        logging.basicConfig(format=formatC, datefmt=datefmt)
    # logging.basicConfig()
    return logging.getLogger(name=name)


class MyLogger(logging.getLoggerClass()):
    def __init__(self, name = "root", level = logging.NOTSET):
        self.debug_color =  BLUEB
        self.info_color = YELLOWB
        self.error_color = REDB
        return super().__init__(name, level)
        
    def debug(self, msg, mth=""):
        super().debug(msg, extra={"color": self.debug_color, "method": mth})
        
    def info(self, msg, mth=""):
        super().info(msg, extra={"color": self.info_color, "method": mth})
        
    def error(self, msg, mth=""):
        super().error(msg, extra={"color": self.error_color, "method": mth})
        
    def change_color(self, method, color):
        setattr(self, f"{method}_color", color)


logging.setLoggerClass(MyLogger)