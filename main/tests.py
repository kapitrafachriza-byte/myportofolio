from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Skill


class MainTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpassword", email="admin@example.com"
        )
        self.regular_user = User.objects.create_user(
            username="regularuser", password="regularpassword"
        )
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami dasar pengembangan web.",
            category="part-time",
        )

    # 1. Halaman profil dapat diakses, memakai index.html,
    #    menampilkan kartu pengalaman, dan memiliki tautan ke halaman Experience.
    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    # 2. URL yang tidak ada mengembalikan 404.
    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    # 3. Model menyimpan dan menghitung is_ongoing dengan benar.
    def test_experience_model_field(self):
        self.assertEqual(self.experience.title, "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    # 4. Halaman Experience menampilkan experience berdasarkan kategori dan
    #    statusnya, serta memiliki tautan kembali ke halaman utama.
    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, "Asisten Dosen PBP")
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    # 5. Halaman Experience menampilkan pesan kondisi kosong apabila belum ada data.
    def test_empty_experience_list(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    # 6. Pengalaman dengan ended_at tidak null menampilkan status Selesai.
    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Selesai")

    # 7. Halaman tambah pengalaman dapat diakses oleh superuser dan memakai create_experience.html.
    def test_create_experience_url_is_accessible(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_experience.html")

    # 8. Form tambah pengalaman berhasil menyimpan data dan me-redirect ke halaman experience.
    def test_create_experience_post_success(self):
        self.client.force_login(self.admin_user)
        data = {
            "title": "Software Engineer Intern",
            "description": "Mengembangkan fitur baru menggunakan Django.",
            "category": "internship",
        }
        response = self.client.post(reverse("main:create_experience"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Software Engineer Intern").exists())

    # 9. Endpoint JSON mengembalikan data dalam format application/json.
    def test_get_experience_json_returns_json(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertTrue(len(response.json()) > 0)

    # 10. Endpoint JSON mendukung query parameter title untuk filtering.
    def test_get_experience_json_filtered_by_title(self):
        response = self.client.get(f"{reverse('main:get_experience_json')}?title=Asisten")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["title"], "Asisten Dosen PBP")

    # 11. Halaman web experience mendukung pencarian via GET query title.
    def test_show_experience_search_filter(self):
        response = self.client.get(f"{reverse('main:show_experience')}?title=Asisten")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Asisten Dosen PBP")

        response_not_found = self.client.get(f"{reverse('main:show_experience')}?title=TidakAda")
        self.assertEqual(response_not_found.status_code, 200)
        self.assertContains(response_not_found, "Tidak ada pengalaman yang cocok")

    # 12. Halaman edit pengalaman dapat diakses oleh superuser dan form ter-populate.
    def test_edit_experience_url_is_accessible(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(
            reverse("main:edit_experience", args=[self.experience.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "edit_experience.html")
        self.assertContains(response, self.experience.title)

    # 13. Form edit berhasil menyimpan perubahan data dan me-redirect ke halaman experience.
    def test_edit_experience_post_success(self):
        self.client.force_login(self.admin_user)
        data = {
            "title": "Asisten Dosen PBP (Updated)",
            "description": "Deskripsi baru.",
            "category": "internship",
            "thumbnail": "",
            "ended_at": "",
        }
        response = self.client.post(
            reverse("main:edit_experience", args=[self.experience.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP (Updated)")
        self.assertEqual(self.experience.category, "internship")

    # 14. View delete menghapus data dan me-redirect ke halaman experience.
    def test_delete_experience_success(self):
        self.client.force_login(self.admin_user)
        experience_id = self.experience.id
        response = self.client.get(
            reverse("main:delete_experience", args=[experience_id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(pk=experience_id).exists())

    # 15. Pengguna biasa (bukan superuser) dilarang menambah atau menghapus pengalaman (403).
    def test_regular_user_forbidden_from_modifications(self):
        self.client.force_login(self.regular_user)
        res_create = self.client.get(reverse("main:create_experience"))
        self.assertEqual(res_create.status_code, 403)

        res_delete = self.client.get(
            reverse("main:delete_experience", args=[self.experience.id])
        )
        self.assertEqual(res_delete.status_code, 403)

    # 16. Pengunjung yang belum login dialihkan ke halaman login saat mencoba menambah pengalaman.
    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))

    # 17. Pengguna yang login dapat memberi star dan unstar pada pengalaman.
    def test_toggle_star_functionality(self):
        self.client.force_login(self.regular_user)
        # Beri star
        response = self.client.post(
            reverse("main:toggle_star", args=[self.experience.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.regular_user, self.experience.starred_by.all())

        # Batalkan star (unstar)
        response_unstar = self.client.post(
            reverse("main:toggle_star", args=[self.experience.id])
        )
        self.assertEqual(response_unstar.status_code, 302)
        self.assertNotIn(self.regular_user, self.experience.starred_by.all())

    # 15. ExperienceForm memiliki field thumbnail dan ended_at.
    def test_experience_form_includes_all_fields(self):
        from main.forms import ExperienceForm
        form = ExperienceForm()
        self.assertIn("thumbnail", form.fields)
        self.assertIn("ended_at", form.fields)
        self.assertIn("title", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("category", form.fields)


class SkillTest(TestCase):

    def setUp(self):
        self.skill = Skill.objects.create(
            name="Python",
            category="programming",
            dot_color="green",
            display_order=0,
        )

    # 7. URL /skills/ dapat diakses dan menggunakan template skills.html.
    def test_skills_url_is_accessible(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")

    # 8. Data skill muncul di halaman HTML ketika ada data.
    def test_skill_data_appears_in_page(self):
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, "Python")
        self.assertContains(response, "dot-green")

    # 9. Halaman menampilkan pesan kondisi kosong ketika belum ada data.
    def test_empty_skill_list(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))
        self.assertContains(response, "Belum ada skill yang ditambahkan.")
