from django.test import TestCase, Client
from django.urls import reverse
from .models import Contact

class ContactModelTest(TestCase):
    def test_contact_creation_and_str(self):
        contact = Contact.objects.create(name="Jane Doe", email="jane@example.com")
        self.assertEqual(str(contact), "Jane Doe")
        self.assertEqual(contact.name, "Jane Doe")
        self.assertEqual(contact.email, "jane@example.com")

class ContactViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact1 = Contact.objects.create(name="Alice Smith", email="alice@example.com")
        self.contact2 = Contact.objects.create(name="Bob Jones", email="bob@example.com")

    def test_contact_list_view(self):
        response = self.client.get(reverse("contacts:contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/index.html")
        self.assertTemplateUsed(response, "contacts/_contact_rows.html")
        self.assertIn("Alice Smith", response.content.decode())
        self.assertIn("Bob Jones", response.content.decode())

    def test_contact_add_view_post(self):
        response = self.client.post(reverse("contacts:contact_add"), {
            "name": "Charlie Brown",
            "email": "charlie@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_rows.html")
        self.assertTrue(Contact.objects.filter(name="Charlie Brown").exists())
        self.assertIn("Charlie Brown", response.content.decode())

    def test_contact_delete_view_success(self):
        delete_url = reverse("contacts:contact_delete", kwargs={"pk": self.contact1.pk})
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertFalse(Contact.objects.filter(pk=self.contact1.pk).exists())

    def test_contact_delete_method_restriction(self):
        delete_url = reverse("contacts:contact_delete", kwargs={"pk": self.contact1.pk})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 405)

    def test_contact_search_view_with_query(self):
        response = self.client.get(reverse("contacts:contact_search"), {"q": "alice"})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Alice Smith", content)
        self.assertNotIn("Bob Jones", content)

    def test_contact_search_view_empty_query(self):
        response = self.client.get(reverse("contacts:contact_search"), {"q": ""})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("Alice Smith", content)
        self.assertIn("Bob Jones", content)

    def test_contact_edit_view(self):
        edit_url = reverse("contacts:contact_edit", kwargs={"pk": self.contact1.pk})
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_edit_row.html")
        content = response.content.decode()
        self.assertIn(f'form="edit-form-{self.contact1.pk}"', content)
        self.assertIn("Alice Smith", content)

    def test_contact_row_view(self):
        row_url = reverse("contacts:contact_row", kwargs={"pk": self.contact1.pk})
        response = self.client.get(row_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_row.html")
        content = response.content.decode()
        self.assertIn("Alice Smith", content)
        self.assertIn("Edit", content)
        self.assertIn("Hapus", content)

    def test_contact_update_view_put(self):
        update_url = reverse("contacts:contact_update", kwargs={"pk": self.contact1.pk})
        put_body = "name=Alice+Wonderland&email=wonderland%40example.com"
        response = self.client.put(
            update_url,
            data=put_body,
            content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts/_contact_row.html")
        self.contact1.refresh_from_db()
        self.assertEqual(self.contact1.name, "Alice Wonderland")
        self.assertEqual(self.contact1.email, "wonderland@example.com")
        self.assertIn("Alice Wonderland", response.content.decode())

    def test_contact_update_method_restriction(self):
        update_url = reverse("contacts:contact_update", kwargs={"pk": self.contact1.pk})
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 405)
