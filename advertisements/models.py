from django.db import models
from users.models import User


class Advertisement(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок объявления",
        help_text="Введите заголовок объявления",
    )
    price = models.PositiveIntegerField(verbose_name="Цена", help_text="Укажите цену")
    description = models.TextField(
        blank=True, null=True, verbose_name="Описание", help_text="Введите описание"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="advertisements",
        verbose_name="Автор объявления",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    advertisement = models.ForeignKey(
        Advertisement,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Объявление",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.author} на {self.advertisement}"
