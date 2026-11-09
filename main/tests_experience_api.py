import uuid
from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from main.models import Experience


class ExperienceAPITest(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_user", password="testpass123", email="owner@example.com"
        )
        self.visitor = User.objects.create_user(
            username="visitor_user", password="testpass123", email="visitor@example.com"
        )
        self.editor_group = Group.objects.create(name="Editor")
        self.editor = User.objects.create_user(
            username="editor_user", password="testpass123", email="editor@example.com"
        )
        self.editor.groups.add(self.editor_group)

        self.experience = Experience.objects.create(
            title="Software Engineering Intern",
            description="Developing backend features with Django and DRF.",
            category="internship",
        )

        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])

        self.payload = {
            "title": "Data Analyst Intern",
            "description": "Analyzing user behavior datasets.",
            "category": "internship",
            "thumbnail": "https://example.com/thumb.png",
        }

    def test_public_can_read_list_and_detail(self):
        # Anonymous user can read list
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(response.data[0]["category_display"], "Internship")

        # Anonymous user can read detail
        detail_response = self.client.get(self.detail_url)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data["title"], "Software Engineering Intern")

    def test_search_and_category_filtering(self):
        response = self.client.get(self.list_url, {"title": "Software"})
        self.assertEqual(len(response.data), 1)

        response_empty = self.client.get(self.list_url, {"title": "nonexistent"})
        self.assertEqual(response_empty.data, [])

        response_cat = self.client.get(self.list_url, {"category": "internship"})
        self.assertEqual(len(response_cat.data), 1)

        response_cat_empty = self.client.get(self.list_url, {"category": "freelance"})
        self.assertEqual(response_cat_empty.data, [])

    def test_guest_and_regular_user_cannot_mutate_and_database_unchanged(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            # Create attempt
            self.assertEqual(
                self.client.post(self.list_url, self.payload, format="json").status_code,
                status.HTTP_403_FORBIDDEN,
            )
            # Update attempt
            self.assertEqual(
                self.client.patch(self.detail_url, {"title": "Malicious Change"}, format="json").status_code,
                status.HTTP_403_FORBIDDEN,
            )
            # Delete attempt
            self.assertEqual(
                self.client.delete(self.detail_url).status_code,
                status.HTTP_403_FORBIDDEN,
            )

        # Verify DB is completely untouched
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Software Engineering Intern")

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        # Editor cannot create
        post_response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

        # Editor cannot delete
        del_response = self.client.delete(self.detail_url)
        self.assertEqual(del_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

        # Editor CAN patch
        patch_response = self.client.patch(
            self.detail_url, {"title": "Updated by Editor"}, format="json"
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated by Editor")

        # Editor CAN put
        put_payload = {
            "title": "Full Update by Editor",
            "description": "Updated description",
            "category": "research",
        }
        put_response = self.client.put(self.detail_url, put_payload, format="json")
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Full Update by Editor")
        self.assertEqual(self.experience.category, "research")

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        # Owner can create
        post_response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        new_id = post_response.data["id"]
        self.assertTrue(Experience.objects.filter(pk=new_id).exists())

        # Owner can update
        patch_response = self.client.patch(
            reverse("api:experience-detail", args=[new_id]),
            {"title": "Owner Patched Title"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)

        # Owner can delete
        del_response = self.client.delete(reverse("api:experience-detail", args=[new_id]))
        self.assertEqual(del_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(del_response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=new_id).exists())

    def test_validation_rejects_empty_or_html_only(self):
        self.client.force_authenticate(user=self.owner)

        invalid_cases = [
            ({"title": "   "}, "title"),
            ({"title": "<script></script>"}, "title"),
            ({"title": "<b>  </b>"}, "title"),
            ({"description": "   "}, "description"),
            ({"description": "<i></i>"}, "description"),
            ({"category": "invalid_choice"}, "category"),
        ]

        for changes, field in invalid_cases:
            bad_payload = {**self.payload, **changes}
            response = self.client.post(self.list_url, bad_payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)

        # Database remains untouched
        self.assertEqual(Experience.objects.count(), 1)

    def test_html_tags_are_stripped(self):
        self.client.force_authenticate(user=self.owner)
        payload = {**self.payload, "title": "<b>Senior Developer</b>"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Senior Developer")

    def test_star_requires_login_and_toggles(self):
        # Anonymous rejected
        anon_res = self.client.post(self.star_url)
        self.assertEqual(anon_res.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated user toggles star on
        self.client.force_authenticate(user=self.visitor)
        res_star = self.client.post(self.star_url)
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertTrue(res_star.data["is_starred"])
        self.assertEqual(res_star.data["star_count"], 1)
        self.assertIn(self.visitor.username, res_star.data["starred_by_names"])

        # Authenticated user toggles star off
        res_unstar = self.client.post(self.star_url)
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertEqual(res_unstar.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        spoofed_payload = {
            **self.payload,
            "star_count": 999,
            "is_starred": True,
            "starred_by_names": "forged_user",
        }
        response = self.client.post(self.list_url, spoofed_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_missing_experience_returns_404(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_wrong_method_returns_405(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner_user", password="testpass123"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner_user", password="testpass123"))
        # Get Browsable API HTML to receive genuine csrf cookie
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value

        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())
