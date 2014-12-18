import random
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from dispatcher.models import Department, DepartmentManager, AlarmLoop, Contact


class GenericViewTestCase(TestCase):
    def setUp(self):
        """
        Create basic database entries:
            - Admin user
            - Test Department
        """
        # create a test admin user
        self.password = 'test'
        self.user = User.objects.create_user(
            'testuser', 'test@test.de', self.password)
        # create a department for this user
        self.department = Department(name='Test Department')
        self.department.save()
        # assign user to department
        self.departmentmanager = DepartmentManager(
            user=self.user, department=self.department)
        self.departmentmanager.save()
        # create some alarm loops
        self.loops = self.helper_model_create_n_loops(12)

    def login(self):
        """
        Login with default admin user.
        """
        login = self.client.login(username=self.user, password=self.password)
        self.failUnless(login, 'Could not log in with user: %s' % self.user)

    def helper_model_create_loop(self, loop, name, text=''):
        a = AlarmLoop(
            loop=loop, name=name, alarm_text=text, department=self.department)
        a.save()
        return a

    def helper_model_create_n_loops(self, n):
        loop_list = []
        for i in range(0, n):
            loop_list.append(
                self.helper_model_create_loop(42000 + i, 'Loop %d' % i))
        return loop_list

    def helper_model_get_n_random_loops(self, n=1):
        return AlarmLoop.objects.order_by('?')[:n]

    def helper_model_create_contact(
            self, firstname, secondname, mail, sms, loop_list=None):
        c = Contact(
            firstname=firstname,
            secondname=secondname,
            mail1=mail,
            sms1=sms,
            department=self.department
            )
        c.save()
        # assign alarm loops
        if loop_list is None:
            # use some random alarm loops (but at least one)
            loop_list = [l.id for l in self.helper_model_get_n_random_loops(
                random.randint(1, len(self.loops)))]
        c.update_alarmloop_assignment(loop_list)
        return c

    def helper_model_create_n_contacts(self, n):
        contact_list = []
        for i in range(0, n):
            contact_list.append(
                self.helper_model_create_contact(
                    'Firstname%d' % i,
                    'Secondname%d' % i,
                    'name.mail%d@host.tld' % i,
                    123456789 + i,
                    ))
        return contact_list


class ContactViewTestCase(GenericViewTestCase):
    def setUp(self):
        super(ContactViewTestCase, self).setUp()

    def test_contact_no_login(self):
        response = self.client.get(
            reverse('dispatcher:contacts'))
        self.assertRedirects(response, "%s?next=%s" % (
            reverse('login'),
            reverse('dispatcher:contacts')))
        response = self.client.get(
            reverse('dispatcher:contacts_create'))
        self.assertRedirects(response, "%s?next=%s" % (
            reverse('login'),
            reverse('dispatcher:contacts_create')))
        response = self.client.get(
            reverse('dispatcher:contacts_update', kwargs={'id': 0}))
        self.assertRedirects(response, "%s?next=%s" % (
            reverse('login'),
            reverse('dispatcher:contacts_update', kwargs={'id': 0})))
        response = self.client.get(
            reverse('dispatcher:contacts_delete', kwargs={'id': 0}))
        self.assertRedirects(response, "%s?next=%s" % (
            reverse('login'),
            reverse('dispatcher:contacts_delete', kwargs={'id': 0})))

    def test_contact_list_without_contacts(self):
        self.login()
        response = self.client.get(reverse('dispatcher:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['contacts'], [])

    def test_contact_list_with_contacts(self):
        self.login()
        # create some contacts in model
        contact_list = self.helper_model_create_n_contacts(10)
        self.assertGreater(len(contact_list), 0)
        # do list request
        response = self.client.get(reverse('dispatcher:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contacts']), len(contact_list))

    def test_contact_create(self):
        self.login()
        # prepare request data
        data = {
            u'firstname': [u'FirstnameNew'],
            u'secondname': [u'SecondnameNew'],
            u'mail1': [u'mail1@host.tld'],
            u'sms1': [u'0171589745236'],
            u'active': True,
            u'test': True,
            u'loops': [str(l.id) for l in
                       self.helper_model_get_n_random_loops(5)],
            }
        # do request
        response = self.client.post(
            reverse('dispatcher:contacts_create'), data)
        self.assertRedirects(response, reverse('dispatcher:contacts'))
        self.assertGreater(Contact.objects.count(), 0)

    def test_contact_update(self):
        self.login()
        # create a contact
        c = self.helper_model_create_contact(
            'FirstName1', 'SecondName1', 'mail1@host.tld', '1234', [1, 2, 3])
        self.assertGreater(Contact.objects.count(), 0)
        # try to change contact data
        data = {
            u'firstname': [u'FirstName2'],
            u'secondname': [u'SecondName2'],
            u'mail1': [u'mail2@host.tld'],
            u'sms1': [u'5678'],
            u'active': False,
            u'test': False,
            u'loops': [u'3', u'4'],
            }
        # do request
        response = self.client.post(
            reverse('dispatcher:contacts_update', kwargs={'id': c.id}), data)
        # assert changes
        self.assertRedirects(response, reverse('dispatcher:contacts'))
        new_c = Contact.objects.get(id=c.id)
        self.assertEqual(new_c.firstname, 'FirstName2')
        self.assertEqual(new_c.secondname, 'SecondName2')
        self.assertEqual(new_c.mail1, 'mail2@host.tld')
        self.assertEqual(new_c.sms1, 5678)
        self.assertEqual(new_c.active, False)
        self.assertEqual(new_c.test, False)
        self.assertEqual(
            [l.id for l in new_c.get_alarmloop_assignment()], [3, 4])

    def test_contact_delete(self):
        self.login()
        # create some contacts
        contact_list = self.helper_model_create_n_contacts(5)
        self.assertGreater(Contact.objects.count(), 0)
        # delete all of them
        for c in contact_list:
            response = self.client.post(
                reverse('dispatcher:contacts_delete', kwargs={'id': c.id}),
                {u'ok': u'ok'})
            self.assertRedirects(response, reverse('dispatcher:contacts'))
        self.assertEqual(Contact.objects.count(), 0)
