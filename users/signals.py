from django.dispatch import receiver
from django.db.models.signals import post_save,m2m_changed
from django.contrib.auth.models import User,Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from events.models import Event
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"


        subject = 'Activate Your Account'
        message = f'Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{activation_url}\n\nThank You!'
        recipient_list = [instance.email]

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")


@receiver(post_save,sender=User)
def assign_role(sender,instance,created, **kwargs):
    if created:
        user_group, created = Group.objects.get_or_create(name ='User')
        instance.groups.add(user_group)
        instance.save()


# @receiver(m2m_changed,sender=Event.participants.through)
# def rsvp_confirmation_mail(sender,instance,action,pk_set, **kwargs):
#     if action == 'post_add':
#         rsvp_users = User.objects.filter(pk__in=pk_set)
#         emails = [user.email for user in rsvp_users]
#         print("checking...",emails)
#         send_mail(
#             subject=f"RSVP confirmation for {instance.name}",
#             message=f"You have been assigned to the task: {instance.title}",
#             from_email='mdasaduzzamanminhaz7@gmail.com',
#             recipient_list=emails,
#             fail_silently= False

#         )
