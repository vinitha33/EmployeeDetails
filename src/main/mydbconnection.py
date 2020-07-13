"""Main production file"""
import csv
import sys
import os
import mysql.connector
import devconfig
import loghandler
import pandas
from pandas import DataFrame


class Connect:
    def __init__(self):
        logger = loghandler.logfile()
        self.logger = logger
    """
    Class to establish the connection to the database
    """
    def connection_db(env):
        """

        :return:
        Returns the connector variable
        """
        try:
            host, user, password, db1 = devconfig.connect(env)
            db = mysql.connector.connect(host=host, user=user, password=password, db=db1)
            logger.info("Database connection established {}@{} with password {}".format
                        (user, host, '*'*len(password)))
            return db
        except Exception as error:
            print(error)


class EmployeeDetails:
    """
    Class to define all the DDL statement in SQL
    """
    def __init__(self, db1):
        logger = loghandler.logfile()
        self.db = db1
        self.logger = logger
        self.cursor = db1.cursor()

    def file_path(self):
        """

        :return:
        Returns the path to the DDL folder
        """
        try:
            folder_path = os.getcwd()
            file_path = os.path.join('\\'.join(folder_path.split('\\')[:-1]), 'files')
            self.logger.info("Path of the DDL folder is fetched")
            return file_path
        except FileNotFoundError as error:
            print(error)
        except Exception as error:
            print(error)
            self.logger.exception("Exception occurred!!!")

    def create_database(self):
        """

        To drop database if exists and create a new database
        """
        try:
            self.cursor.execute("DROP DATABASE IF EXISTS mymodel")
            self.logger.info("Existing database dropped")
            self.cursor.execute("CREATE DATABASE mymodel")
            self.logger.info("New databasae created")
            self.cursor.execute("USE mymodel")
            self.db.commit()
        except Exception as e:
            print(e)

        self.create_table()

    def create_table(self):
        """

        :param
         name: name of the table to create
        :return:
        return the function to insert values into the table
        """
        try:
            file_path1 = self.file_path()
            for filename in os.listdir(file_path1):
                if filename.split('.')[1] == 'sql':
                    file_open = open(os.path.join(file_path1, filename))
                    lines = file_open.read().split(';')
                    self.cursor.execute(lines[0])
                    self.db.commit()
                    self.logger.info(filename.split('.')[0]+" table created")
            self.logger.info("Table creation completed!!")
        except Exception as error:
            print(error)
        self.insert_db()

    def insert_db(self):
        """
        :return:
        A function to fetch records from CSV and put it into the database
        """

        try:
            file_path1 = self.file_path()
            self.cursor.execute("SELECT table_name FROM information_schema.tables"
                                " WHERE table_schema='mymodel'")
            table_name = self.cursor.fetchall()
            table_names = []
            for i in table_name:
                for j in i:
                    table_names.append(j)
            num1 = len(table_names)
            for i in range(num1):
                for filename in os.listdir(file_path1):
                    if filename.split('.')[1] == 'csv' and filename.split('.')[0] == table_names[i]:
                        self.cursor.execute("SELECT column_name FROM information_schema.columns"
                                            " where table_schema='mymodel' and table_name='{}'".format
                                            (table_names[i]))
                        len_ins = self.cursor.fetchall()
                        ins_len = len(len_ins)
                        file_open = open(os.path.join(file_path1, filename))
                        data = csv.reader(file_open)
                        for datas in data:
                            self.cursor.execute("INSERT INTO {} VALUES ({})".format
                                                (table_names[i], ','.join(['%s' for num in range
                                                (ins_len)])), datas)
                            self.db.commit()
                        self.logger.info("Values inserted in table - "+ filename.split('.')[0])
            self.logger.info("Insertion completed!!")

        except Exception as e:
            print(e)

    def query_db(self):
        print("********ENTER YOUR CHOICE********")
        choice = input("1: To print department details and branch details of each employee\n"
                       "2: To print the number of employees for each skill\n"
                       "3: Exit\n")
        if choice == '1':
            self.query1()
        elif choice == '2':
            self.query2()
        else:
            exit()

    def query1(self):
        try:
            sql = "SELECT e.emp_id ,e.e_name ,p.branch_id,b.facility ," \
                  "b.state AS STATE, d.d_name AS DEPT_NAME from " \
                  "zemp_project p LEFT join employee e  ON p.emp_id=e.emp_id " \
                  "left outer join branch_location b  on p.branch_id=b.branch_id " \
                  "left outer join department d on p.dept_id=d.dept_id;"
            self.cursor.execute(sql)
            cc = self.cursor.fetchall()
            self.db.commit()
            print(cc)
            df = DataFrame(cc, columns=['EMP_ID', 'EMPLOYEE_NAME', 'BRANCH_ID', 'FACILITY', 'STATE', 'DEPT_NAME'])
            html = df.to_html()
            text_file = open("emp_branch_facility.html", "w")
            text_file.write(html)
            text_file.close()
            return cc
        except Exception as e:
            print(e)

    def query2(self):
        try:
            sql = "select s.skill_name, count(e.e_name) from zemp_hike h join" \
                  " skill_set s on h.skill_id = s.skill_id join employee e on" \
                  " h.emp_id = e.emp_id group by s.skill_name";
            self.cursor.execute(sql)
            cc = self.cursor.fetchall()
            self.db.commit()
            print(cc)
            df = DataFrame(cc, columns=['Skill Name', 'No of Employees'])
            html = df.to_html()
            text_file = open("employee_count_in_each_skill.html", "w")
            text_file.write(html)
            text_file.close()

        except Exception as e:
            print(e)

if __name__ == '__main__':
    logger = loghandler.logfile()
    envi = sys.argv[1]

    db1 = Connect.connection_db(envi)
    c_obj = EmployeeDetails(db1)
    c_obj.create_database()
    c_obj.query_db()