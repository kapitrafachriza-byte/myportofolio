from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.html import strip_tags
from main.models import Experience


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ["title", "description", "category", "thumbnail", "ended_at"]

    def clean_title(self):
        title = strip_tags(self.cleaned_data.get("title", "")).strip()
        if not title:
            raise ValidationError("Judul pengalaman tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        description = strip_tags(self.cleaned_data.get("description", "")).strip()
        if not description:
            raise ValidationError("Deskripsi tidak boleh hanya berisi tag HTML.")
        return description

