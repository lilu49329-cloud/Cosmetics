from django.db import models

class Slider(models.Model):
    title = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='slider/', blank=False)
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Slider/Banner'
        verbose_name_plural = 'Sliders/Banners'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Slider #{self.id}"
