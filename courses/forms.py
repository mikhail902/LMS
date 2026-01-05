from django import forms
from prompt_toolkit.validation import ValidationError

from .models import Lesson


class LessonForm(forms.ModelForm):
    FORBIDDEN_WORDS = [
        "казино",
        "биржа",
        "обман",
        "криптовалюта",
        "дешево",
        "полиция",
        "крипта",
        "бесплатно",
        "радар",
    ]

    class Meta:
        model = Lesson
        exclude = ("owner", "status_published")

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите название"}
        )
        self.fields["pic"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберете фото"}
        )
        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Напишите описание"}
        )
        self.fields["category"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Выберете категорию"}
        )
        self.fields["price"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите цену"}
        )
        self.fields["created_at"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите дату создания"}
        )
        self.fields["updated_at"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Введите дату последнего изменения",
            }
        )

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price < 0 or price is None:
            raise ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def check_forbidden_words(self, text, field_name):
        """Вспомогательный метод для проверки запрещенных слов"""
        if not text:
            return
        text_lower = text.lower()
        for forbidden_word in self.FORBIDDEN_WORDS:
            if forbidden_word in text_lower:
                raise ValidationError(
                    f'В поле "{field_name}" обнаружено запрещенное слово: "{forbidden_word}". '
                    f"Пожалуйста, измените текст."
                )

    def clean_name(self):
        """Валидация названия - проверка на запрещенные слова"""
        name = self.cleaned_data.get("name")
        self.check_forbidden_words(name, "Название")
        return name

    def clean_description(self):
        """Валидация описания - проверка на запрещенные слова"""
        description = self.cleaned_data.get("description")
        self.check_forbidden_words(description, "Описание")
        return description


class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["description", "category"]
