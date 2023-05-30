import unittest
from tkinter import Tk
from tkinter.messagebox import *
from tkinter.ttk import *
from tkcalendar import DateEntry

from school_management_system import *

class TestSchoolManagementSystem(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.update()
        self.root.destroy()

    def test_reset_fields(self):
        self.name_strvar.set('John')
        self.email_strvar.set('john@example.com')
        self.contact_strvar.set('1234567890')
        self.gender_strvar.set('Male')
        self.dob.set_date(self.datetime.date(2000, 1, 1))
        self.stream_strvar.set('Science')

        self.reset_fields()

        self.assertEqual(self.name_strvar.get(), '')
        self.assertEqual(self.email_strvar.get(), '')
        self.assertEqual(self.contact_strvar.get(), '')
        self.assertEqual(self.gender_strvar.get(), '')
        self.assertEqual(self.dob.get_date(), datetime.datetime.now().date())
        self.assertEqual(self.stream_strvar.get(), '')

    def test_reset_form(self):
        self.tree.insert('', self.END, values=(1, 'John', 'john@example.com', '1234567890', 'Male', '2000-01-01', 'Science'))
        self.reset_form()

        self.assertEqual(len(self.tree.get_children()), 0)
        self.assertEqual(self.name_strvar.get(), '')
        self.assertEqual(self.email_strvar.get(), '')
        self.assertEqual(self.contact_strvar.get(), '')
        self.assertEqual(self.gender_strvar.get(), '')
        self.assertEqual(self.dob.get_date(), self.datetime.datetime.now().date())
        self.assertEqual(self.stream_strvar.get(), '')

    def test_display_records(self):
        self.cursor.execute("DELETE FROM SCHOOL_MANAGEMENT")
        self.cursor.execute("INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (%s,%s,%s,%s,%s,%s)",
                       ('John', 'john@example.com', '1234567890', 'Male', '2000-01-01', 'Science'))
        self.cursor.execute("INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (%s,%s,%s,%s,%s,%s)",
                       ('Jane', 'jane@example.com', '9876543210', 'Female', '1999-12-31', 'Arts'))
        self.connector.commit()

        self.display_records()

        self.assertEqual(len(self.tree.get_children()), 2)

    def test_add_record(self):
        self.cursor.execute("DELETE FROM SCHOOL_MANAGEMENT")
        self.connector.commit()

        self.name_strvar.set('John')
        self.email_strvar.set('john@example.com')
        self.contact_strvar.set('1234567890')
        self.gender_strvar.set('Male')
        self.dob.set_date(self.datetime.date(2000, 1, 1))
        self.stream_strvar.set('Science')

        self.add_record()

        self.cursor.execute('SELECT * FROM SCHOOL_MANAGEMENT')
        data = self.cursor.fetchall()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][1], 'John')
        self.assertEqual(data[0][2], 'john@example.com')
        self.assertEqual(data[0][3], '1234567890')
        self.assertEqual(data[0][4], 'Male')
        self.assertEqual(data[0][5], '2000-01-01')
        self.assertEqual(data[0][6], 'Science')

    def test_remove_record(self):
        self.cursor.execute("DELETE FROM SCHOOL_MANAGEMENT")
        self.cursor.execute("INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (%s,%s,%s,%s,%s,%s)",
                       ('John', 'john@example.com', '1234567890', 'Male', '2000-01-01', 'Science'))
        self.connector.commit()

        self.tree.selection_set(self.tree.get_children()[0])

        self.remove_record()

        self.cursor.execute('SELECT * FROM SCHOOL_MANAGEMENT')
        data = self.cursor.fetchall()
        self.assertEqual(len(data), 0)
        self.assertEqual(len(self.tree.get_children()), 0)

    def test_view_record(self):
        self.cursor.execute("DELETE FROM SCHOOL_MANAGEMENT")
        self.cursor.execute("INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, DOB, STREAM) VALUES (%s,%s,%s,%s,%s,%s)",
                       ('John', 'john@example.com', '1234567890', 'Male', '2000-01-01', 'Science'))
        self.connector.commit()

        self.tree.selection_set(self.tree.get_children()[0])

        self.view_record()

        self.assertEqual(self.name_strvar.get(), 'John')
        self.assertEqual(self.email_strvar.get(), 'john@example.com')
        self.assertEqual(self.contact_strvar.get(), '1234567890')
        self.assertEqual(self.gender_strvar.get(), 'Male')
        self.assertEqual(self.dob.get_date(), self.datetime.date(2000, 1, 1))
        self.assertEqual(self.stream_strvar.get(), 'Science')

if __name__ == '__main__':
    unittest.main()
