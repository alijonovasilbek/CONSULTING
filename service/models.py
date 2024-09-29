# from django.db import models
#
# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
#
#
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     prize_inviting = models.IntegerField(blank=True, null=True)
#     profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
#
#     def __str__(self):
#         return f"{self.user.username}'s profile"
#
#     class Meta:
#         db_table = 'user_profile'
#
#
#
# class Referral(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     referral_code = models.CharField(max_length=20, unique=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.user.username} - {self.referral_code}'
#
#     class Meta:
#         db_table = 'referral'
#
#
# class Reffered(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     referred_by = models.ForeignKey(Referral, null=True, blank=True, on_delete=models.SET_NULL)
#     date_invited = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'reffered'
#
#
#
# class ContactMessage(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     subject = models.CharField(max_length=200)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Message from {self.name} ({self.email})"
#
#     class Meta:
#         db_table = 'contact_message'
#
