from django.db import models
from App_login.models import CustomUser


class ShopManagerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10)
    nid = models.CharField(max_length=17)
    NID_front_photo = models.ImageField(upload_to='nid_photo/')
    NID_back_photo = models.ImageField(upload_to='nid_photo/')
    photo = models.ImageField(upload_to='profile_photos/')
    permanent_address = models.CharField(max_length=255)
    present_address = models.CharField(max_length=255)
    emergency_contact = models.CharField(max_length=17)
    status = models.BooleanField(default=True)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self.generate_employee_id()

        super().save(*args, **kwargs)

    def generate_employee_id(self):
        count = ShopManagerProfile.objects.count()
        return f"spm-{count + 1}"
