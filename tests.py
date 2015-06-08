import unittest, matchmaker

class MyTest(unittest.TestCase):
    def test_person(self):
        person = matchmaker.Person("person1", [1, 2, 3], is_driver=True, size=2, is_site_leader=True)
        self.assertEqual(person.name, "person1")
        self.assertEqual(person.available_times, [1,2,3])
        self.assertTrue(person.is_driver)
        self.assertEqual(person.size, 2)
        self.assertTrue(person.is_site_leader)

    def test_site(self):
        site = matchmaker.Site("site1", meeting_time=1, capacity=4)
        self.assertEqual(site.name, "site1")
        self.assertEqual(site.meeting_time, 1)
        self.assertEqual(site.capacity, 4)

if __name__ == '__main__':
    unittest.main()
