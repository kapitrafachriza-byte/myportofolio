from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience


class MainTest(TestCase):

    def setUp(self):
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
