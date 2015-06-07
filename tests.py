import unittest, matchmaker

class MyTest(unittest.TestCase):
    def test_person(self):
        self.person = matchmaker.Person("person1", [1, 2, 3], is_driver=True, size=2, is_site_leader=True)
        self.assertEqual(self.person.name, "person1")
        self.assertEqual(self.person.available_times, [1,2,3])
        self.assertTrue(self.person.is_driver)
        self.assertEqual(self.person.size, 2)
        self.assertTrue(self.person.is_site_leader)

if __name__ == '__main__':
    unittest.main()
