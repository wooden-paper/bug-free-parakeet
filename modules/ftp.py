# Author: Joseph.Y
"""This program is an API for the simple FTP client that allows the user to connect to a server and download files from it.
The user can specify the names of the files to download and the server to connect to.
The program will then download the files and save them in the current directory.
"""
from ftplib import FTP
import os
from threading import Thread, Event
from queue import Queue, Empty

"""
Class for the FTP client. It is an API for the FTP client that allows the user to connect to a server and download files from it.
"""


class MyFTP:
    def __init__(self, host, username, password):
        """
        The __init__ function is called automatically every time the class is
        instantiated. In this case, the __init__ function initializes an FTP connection by connecting to a host and
        logging in as a user with a password.

        :param self: Refer to the object itself
        :param host: Store the host name
        :param username: Set the username for the ftp connection
        :param password: Set the password for the ftp connection
        """
        self.host = host
        self.username = username
        self.password = password
        self.ftp = FTP(self.host)
        self.ftp.login(user=self.username, passwd=self.password)
        self.ftp.set_pasv(True)

    def set_pasv(self, mode):
        """
        The set_pasv function sets the mode of operation to passive or active.
        Passive mode is used for PASV, while active is used for PORT and EPRT.


        :param self: Reference the instance of the object itself
        :param mode: Set the mode of data transfer to passive or active, true or false
        """
        self.ftp.set_pasv(mode)

    # File transfer methods
    """
    Method for downloading every file in the current directory.
    """

    def download_all_files(self, download_path):
        """
        The download_all_files function downloads all files from the FTP server to a specified download path.

        :param self: Allow the function to refer to the ftp object
        :param download_path: Specify the path where the files will be downloaded to
        """
        filenames = self.ftp.nlst()  # get filenames within the directory
        for filename in filenames:
            local_filename = os.path.join(download_path, filename)
            file = open(local_filename, "wb")
            self.ftp.retrbinary("RETR " + filename, file.write)
            file.close()

    def getBytes(self, filename):
        print("getBytes")
        self.ftp.retrbinary("RETR {}".format(filename), self.bytes.put)
        self.bytes.join()  # wait for all blocks in the queue to be marked as processed
        self.finished.set()  # mark streaming as finished

    def sendBytes(self):
        while not self.finished.is_set():
            try:
                yield self.bytes.get(timeout=self.timeout)
                self.bytes.task_done()
            except Empty:
                self.finished.wait(self.timeout)
        self.worker.join()

    def download(self, filename):
        self.bytes = Queue()
        self.finished = Event()
        self.worker = Thread(target=self.getBytes, args=(filename,))
        self.worker.start()
        return self.sendBytes()

    # Directory traversal methods
    """
    Method for changing the directory on the server.
    """

    def change_directory(self, directory):
        """
        The change_directory function changes the current working directory to the specified path.

        :param self: Access variables that belongs to the class
        :param directory: Specify the directory to change to
        """
        self.ftp.cwd(directory)

    """
    Method for getting the current directory on the server.
    """

    def get_current_directory(self):
        """
        The get_current_directory function returns the current working directory.


        :param self: Access variables that belongs to the class
        :return: The current working directory
        """
        return self.ftp.pwd()

    """
    Method for getting the list of files in the current directory on the server.
    """

    def get_files_in_current_directory(self):
        """
        The get_files_in_current_directory function returns a list of all files in the current directory.


        :param self: Access the attributes and methods of the class in python
        :return: A list of files in the current directory
        """
        return self.ftp.nlst()

    """
    Method for getting the list of files in the specified directory on the server.
    """

    def get_files_in_directory(self, directory):
        """
        The get_files_in_directory function accepts a directory name as an argument and returns a list of files in that directory.


        :param self: Reference the instance of the class
        :param directory: Specify the directory to search for files in
        :return: A list of files in the directory
        """
        self.ftp.cwd(directory)
        return self.ftp.nlst()

    # Connection methods
    """
    Method for closing the connection to the current server.
    """

    def close_connection(self):
        """
        The close_connection function closes the connection to the database.

        :param self: Refer to the object that is calling the function
        """
        self.ftp.close()

    """
    Method for opening a connection to a new server.
    """

    def open_connection(self, host, username, password):
        """
        Method for opening a connection to a new server.
        :param self: Reference the class itself
        :param host: Specify the server name or ip address
        :param username: Specify the username to use when connecting to the remote computer
        :param password: Pass the password to the connect function
        """
        self.__init__(host, username, password)
