import tkinter
import os
import logging
import logging.handlers
import model.model as model

from tkinter import messagebox
from views.mainView import MainView
from model.model import db


class Controller():

    logger = logging.getLogger('app_logger')

    def __init__(self):
        # Create logger object and configure it
        self.setupLogger()
        self.logger.info("Logger inicializado com sucesso")

        # Setup database using ORM
        self.setupDatabase()
        self.logger.info("Banco de dados inicializado com sucesso")

    def setupDatabase(self):
        """Sets up the database connection and creates tables"""
        db.connect()
        model.create_tables()
        db.close()

    def setupLogger(self, level=logging.DEBUG):
        """Sets up the logger object. Logging level, filename, handlers and formatters"""
        self.logger.setLevel(level)
        formatter = logging.Formatter(fmt='%(asctime)s %(module)-16s %(levelname)-8s <%(funcName)s> %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S')
        try:
            filename = os.path.join(self.createLogDir(), "estoque.log")
            log_file_handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when='midnight', interval=1)
            log_file_handler.setLevel(logging.DEBUG)
            log_file_handler.setFormatter(formatter)
            self.logger.addHandler(log_file_handler)

            log_output_handler = logging.StreamHandler()
            log_output_handler.setLevel(logging.WARNING)
            log_output_handler.setFormatter(formatter)
            self.logger.addHandler(log_output_handler)
            return 0
        except TypeError:
            print("Log directory is NoneType")
            return 1

    def createLogDir(self, logDir="logs"):
        """Creates, if non-existant, and returns the application's log path"""
        logPath = os.path.join(os.getcwd(), logDir)
        if os.path.exists(logPath):
            print("Log path already exists")
            return logPath
        else:
            try:
                os.mkdir(logPath)
                return logPath
            except OSError:
                print("Unable to create log path")
                return None

    def createNewProduct(self):
        messagebox.showinfo("Info", "Novo produto criado")

    def deleteProduct(self):
        messagebox.showinfo("Info", "Produto excluído")

    def addUnitsToProduct(self):
        messagebox.showinfo("Info", "Unidades adicionadas")

    def removeUnitsFromProduct(self):
        messagebox.showinfo("Info", "Unidades removidas")

    def run(self):
        root = tkinter.Tk()
        view = MainView(root, self)
        root.mainloop()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
