"""Unit testing file"""
import sys
import os
import unittest

sys.path.append("C:\\Users\\vinitha.muralidharan\\PycharmProjects\\EmployeeDetails\\src\\main")
import mydbconnection


class TestDatabaseConnection(unittest.TestCase):
    """
    CLASS TO PERFORM UNIT TESTING FOR INITIATING TESTS FOR EACH MODULE
    """

    def test_connection_db(self):
        """

        Test to check if the database connection is getting established
        """
        obj = mydbconnection.Connect()
        self.assertIsNotNone(obj.connection_db('dev'))

    def test_file_path(self):
        """

        Test to check if the file path of the .sql and .csv files are getting fetched
        """
        file_path = os.path.dirname(os.path.dirname(__file__)) + "\\files"
        file_path1 = os.path.dirname(os.path.dirname(__file__))
        self.assertTrue(file_path, mydbconnection.EmployeeDetails.file_path(self))
        self.assertFalse(file_path1, mydbconnection.EmployeeDetails.file_path(self))

    def test_create_table(self):
        """

        Test to check if tables are getting created in the database
        """
        db1 = mydbconnection.Connect.connection_db('dev')
        cursor = db1.cursor()
        folder_path = os.getcwd()
        file_path = os.path.join('\\'.join(folder_path.split('\\')[:-1]), 'files')
        cursor.execute("SELECT table_name FROM information_schema.tables"
                       " WHERE table_schema='mymodel'")
        table_name = cursor.fetchall()
        table_names = []
        for i in table_name:
            for j in i:
                table_names.append(j)
        num1 = len(table_names)
        for i in range(num1):
            for filename in os.listdir(file_path):
                if filename.split('.')[1] == 'sql' and filename.split('.')[0] == table_names[i]:
                    self.assertEqual(filename.split('.')[0], table_names[i])
                    self.assertNotEqual(filename.split('.')[1], table_names[i])

    # def test_Query_table(self):
    #     db1 = mydbconnection.Connect.connection_db('dev')
    #     cursor = db1.cursor()
    #     a = mydbconnection.EmployeeDetails.query1(self)
    #     sql = "SELECT e.emp_id ,e.e_name ,p.branch_id,b.facility ," \
    #           "b.state AS STATE, d.d_name AS DEPT_NAME from " \
    #           "zemp_project p LEFT join employee e  ON p.emp_id=e.emp_id " \
    #           "left outer join branch_location b  on p.branch_id=b.branch_id " \
    #           "left outer join department d on p.dept_id=d.dept_id;"
    #     cursor.execute(sql)
    #     res = cursor.fetchall()
    #     # self.assertEqual(a, res)

    # def test_insert_table(self):
    #     db1 = mydbconnection.Connect.connection_db('dev')
    #     cursor = db1.cursor()
    #     folder_path = os.getcwd()


if __name__ == '__main__':
    unittest.main()
