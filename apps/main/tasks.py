from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailSubscription, News


@shared_task
def send_news_notification_email(news_id, school_id):
    """
    Send news notification email to all subscribed users of a school
    """
    try:
        # Get the news object
        news = News.objects.get(id=news_id, school_id=school_id)
        
        # Get all active email subscriptions for this school
        subscriptions = EmailSubscription.objects.filter(
            school_id=school_id, 
            is_active=True
        )
        
        if not subscriptions.exists():
            return f"No active subscriptions found for school {school_id}"
        
        # Prepare email content
        subject = f"Yangi xabar: {news.title}"
        
        # Create HTML email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">
                    {news.title}
                </h2>
                <div style="margin: 20px 0;">
                    <strong>Sana:</strong> {news.created_at.strftime('%d.%m.%Y')}
                </div>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    {news.content}
                </div>
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
                    <p>Bu xabar {news.school.name} tomonidan yuborildi.</p>
                    <p>Obunani bekor qilish uchun maktab bilan bog'laning.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create plain text version
        plain_content = f"""
        {news.title}
        
        Sana: {news.created_at.strftime('%d.%m.%Y')}
        
        {strip_tags(news.content)}
        
        ---
        Bu xabar {news.school.name} tomonidan yuborildi.
        Obunani bekor qilish uchun maktab bilan bog'laning.
        """
        
        # Send emails to all subscribers
        email_list = list(subscriptions.values_list('email', flat=True))
        
        # Send email using Django's send_mail
        emails_sent = 0
        for email in email_list:
            try:
                send_mail(
                    subject=subject,
                    message=plain_content,
                    from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@bmsb.uz',
                    recipient_list=[email],
                    html_message=html_content,
                    fail_silently=False,
                )
                emails_sent += 1
            except Exception as e:
                print(f"Failed to send email to {email}: {str(e)}")
                continue
        
        return f"Successfully sent {emails_sent} emails out of {len(email_list)} for news '{news.title}'"
        
    except News.DoesNotExist:
        return f"News with id {news_id} not found"
    except Exception as e:
        return f"Error sending emails: {str(e)}"


@shared_task
def test_email_task():
    """
    Simple test task to verify Celery is working
    """
    return "Celery is working correctly!" 