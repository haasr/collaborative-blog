from asyncore import write
from re import sub
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime as dt, timedelta
import tzlocal

from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMessage
from admin_pages.models import NewsletterSendFailure, Post, SEO, SubscriberNewsletter, SubscribeFormSettings
from .models import EmailSubscriber
from custom_template_tags.texttransform.templatetags import texttransform
from anymail.exceptions import *

from os import system

active_newsletter = None

domain = Site.objects.get_current().domain

seo = SEO.objects.get(id=1)
site_name = seo.meta_title

subscriber_newsletter = SubscriberNewsletter.objects.get(id=1)
subscribe_form_settings = SubscribeFormSettings.objects.get(id=1)

# Yeah, I don't feel like commenting this anytime soon.
# Cooler stuff to do XD


class NewsletterSender:
    form_failures = {}
    f_id = -2147483648


    def stash_failure(to, template_used, template_id):
        try:
            NewsletterSender.f_id +=1
        except: # Int range exceeded
            NewsletterSender.f_id = -2147483648
        f = NewsletterSendFailure(
                to=to,
                template_used=template_used,
                template_id=template_id,
                exception='Uncaptured',
        )
        NewsletterSender.form_failures[NewsletterSender.f_id] = f
        return NewsletterSender.f_id


    def save_failure(id, ex='None'):
        f = NewsletterSender.form_failures.pop(id)
        f.exception = str(ex)[:500] # Truncate to fit model max
        f.save()


    def send(to, template_used, template_id, message):
        f_id = NewsletterSender.stash_failure(to, template_used, template_id)
        try:
            message.send(fail_silently=False)
            NewsletterSender.form_failures.pop(f_id)
        except (AnymailRequestsAPIError, AnymailRecipientsRefused, AnymailInvalidAddress,
            AnymailSerializationError, AnymailUnsupportedFeature) as ex:
            NewsletterSender.save_failure(f_id, ex)
        except Exception as ex:
            NewsletterSender.save_failure(f_id, ex)
        try:
            NewsletterSender.form_failures.pop(f_id)
        except: # Already popped
            pass


class Newsletter:
    def __init__(self):
        global subscriber_newsletter

        self.custom_message=subscriber_newsletter.custom_message
        self.num_featured_posts=subscriber_newsletter.num_featured_posts
        self.num_recent_posts=subscriber_newsletter.num_recent_posts
        self.send_interval=subscriber_newsletter.send_interval
        self.day=subscriber_newsletter.week_send_day
        self.hour=subscriber_newsletter.send_hour
        self.minute=subscriber_newsletter.send_minute
        self._job_id = None
        self.scheduled = False
        self.send_time = "None"
        self.unsubscribe_url=subscriber_newsletter.unsubscribe_url

    def __str__(self):
        return (
            f"{self.send_interval}ly newsletter:\n"
            f"  scheduled: {self.scheduled}"
            f"  send time: {self.send_time}"
            f"  unsubscribe URL:  {self.unsubscribe_url}"
        )


class WeeklyNewsletter(Newsletter):
    # Defaults day to Saturday if unspecified
    def __init__(self):
        global subscriber_newsletter

        super().__init__()
        self.send_time = f"{self.hour}:{self.minute} on {self.day}"

    def update(self):
        global subscriber_newsletter

        if self.scheduled:
            message = "WeeklyNewsletter: Update refused. Remove the scheduled job before updating"
            return False, message
        else:
            self.custom_message=subscriber_newsletter.custom_message
            self.num_featured_posts=subscriber_newsletter.num_featured_posts
            self.num_recent_posts=subscriber_newsletter.num_recent_posts
            self.send_interval=subscriber_newsletter.send_interval
            self.day=subscriber_newsletter.week_send_day
            self.hour=subscriber_newsletter.send_hour
            self.minute=subscriber_newsletter.send_minute

            self.send_time = f"{self.hour}:{self.minute} on {self.day}"

            message = "WeeklyNewsletter: Updated"
            return True, message


class MonthlyNewsletter(Newsletter):
    # Defaults day to Saturday if unspecified
    def __init__(self):
        super().__init__()
        self.send_time = f"{self.hour}:{self.minute} monthly"

    def update(self):
        global subscriber_newsletter

        if self.scheduled:
            message = "MonthlyNewsletter: Update refused. Remove the scheduled job before updating"
            return False, message
        else:
            self.custom_message=subscriber_newsletter.custom_message
            self.num_featured_posts=subscriber_newsletter.num_featured_posts
            self.num_recent_posts=subscriber_newsletter.num_recent_posts
            self.send_interval=subscriber_newsletter.send_interval
            self.day=subscriber_newsletter.week_send_day
            self.hour=subscriber_newsletter.send_hour
            self.minute=subscriber_newsletter.send_minute

            self.send_time = f"{self.hour}:{self.minute} on {self.day}"

            message = "MonthlyNewsletter: Updated"
            return True, message


class BackgroundNewsletterScheduler(BackgroundScheduler):
    __instance = None

    WEEKDAYS = {
        0: 'mon',
        1: 'tue',
        2: 'wed',
        3: 'thu',
        4: 'fri',
        5: 'sat',
        6: 'sun'
    }

    def __init__(self):
        super().__init__(timezone=str(tzlocal.get_localzone()))
        self.start()
        self.update_newsletter()

    def __new__(cls):
        if BackgroundNewsletterScheduler.__instance is None:
            BackgroundNewsletterScheduler.__instance = object.__new__(cls)
        return BackgroundNewsletterScheduler.__instance


    def retreive_posts(self, posts, num_featured, num_recent):
        featured_posts = {}
        recent_posts = {}
        featured_posts_list = []
        recent_posts_list = []
        featured_gt_zero = (num_featured > 0)
        recent_gt_zero = (num_recent > 0)

        if featured_gt_zero:
            featured_posts = posts.filter(is_featured=True)[:num_featured]
            if recent_gt_zero: # Since these are both nonzero, don't show any of the same in recent
                recent_posts = posts.filter(is_featured=False)[:num_recent]
        else: # 0 featured posts
            if recent_gt_zero: # Since featured is zero, don't need to filter out featured posts
                recent_posts = posts[:num_recent]

        for post in featured_posts:
            box_text = texttransform.remove_headers(post.box_content_text[:500])
            text = (f"<h2>{post.title}</h2>\n" +
                    f"<h4>by {post.author.preferred_name}</h4>\n\n" +
                    box_text + '...<hr>')
            featured_posts_list.append(text)

        for post in recent_posts:
            box_text = texttransform.remove_headers(post.box_content_text[:500])
            text = (f"<h2>{post.title}</h2>\n" +
                    f"<h4>by {post.author.preferred_name}</h4>\n\n" +
                    box_text + '...<hr>')
            recent_posts_list.append(text)

        featured_gt_zero = len(featured_posts) > 0
        recent_gt_zero = len(recent_posts) > 0

        return featured_gt_zero, recent_gt_zero, featured_posts_list, recent_posts_list


    def send_newsletter(self, newsletter):
        global subscriber_newsletter
        now = dt.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        subscribers = list(EmailSubscriber.objects.values_list('email_addr', 'first_name'))
        if newsletter.send_interval == 'month':
            last_month_time = (now - timedelta(days=8)) # Need to go back to around the end of last month

            # Get last month's posts
            posts = Post.objects.filter(visibility='public', og_date__year=last_month_time.year,
                                        og_date__month=last_month_time.month).order_by('-og_date')
        else:
            start_date = 0
            if newsletter.day > 0:
                start_date = now - timedelta(days=newsletter.day)
            end_date = 6
            if newsletter.day < 6:
                end_date = now + timedelta(days=newsletter.day)

            posts = Post.objects.filter(visibility='public', og_date__gte=start_date,
                                        og_date__lte=end_date).order_by('-og_date')

        featured_gt_zero, \
        recent_gt_zero, \
        featured_posts_list, \
        recent_posts_list = self.retreive_posts(posts, newsletter.num_featured_posts,
                                                    newsletter.num_recent_posts)

        both_zero = (not featured_gt_zero) and (not recent_gt_zero)

        template_used = 'Featured & Recent'
        template_id = subscriber_newsletter.both_template_id # Featured and recent
        if not both_zero: # Don't bother sending a newsletter if no new posts
            if not recent_gt_zero:
                template_id = subscriber_newsletter.featured_template_id
                template_used = 'Featured'
            elif not featured_gt_zero:
                template_id = subscriber_newsletter.recent_template_id
                template_used = 'Recent'

            title = (
                f"{site_name}: {newsletter.send_interval[0].upper()}"
                f"{newsletter.send_interval[1:]}ly Newsletter"
            )

            formdata = {
                'title': title,
                'message': newsletter.custom_message,
                'featured_posts': featured_posts_list,
                'recent_posts': recent_posts_list
            }

            for sub in subscribers:
                formdata['email'] = sub[0]
                formdata['name'] = sub[1]
                formdata['unsubscribe_url'] = newsletter.unsubscribe_url + sub[0],
                message = EmailMessage(to=[ sub[0] ])
                message.template_id = template_id
                message.from_email = None
                message.merge_global_data = formdata

                NewsletterSender.send(sub[0], template_used, template_id, message)


    def add_weekly_newsletter(self, newsletter):
        cr_trigger = CronTrigger(
            day_of_week=newsletter.day,
            hour=newsletter.hour,
            minute=newsletter.minute
        )
        job = self.add_job(func=self.send_newsletter, trigger=cr_trigger,
                            args=[newsletter])

        # Update the newsletter object to show that it is scheduled
        # and store the job ID so the newsletter can be removed if needed:
        newsletter._job_id = job.id
        newsletter.scheduled = True


    def add_monthly_newsletter(self, newsletter):
        send_day = f"1st {BackgroundNewsletterScheduler.WEEKDAYS[newsletter.day]}"
        job = self.add_job(
            func=self.send_newsletter, trigger='cron', day=send_day,
            hour=newsletter.hour, minute=newsletter.minute, args=[newsletter]
        )

        # Update the newsletter object to show that it is scheduled
        # and store the job ID so the newsletter can be removed if needed:
        newsletter._job_id = job.id
        newsletter.scheduled = True


    def remove_newsletter(self, newsletter):
        if newsletter.scheduled:
            try:
                self.remove_job(newsletter._job_id)
            except:
                pass
            newsletter.scheduled = False


    def add_newsletter(self):
        global active_newsletter
        global subscriber_newsletter

        if subscriber_newsletter.send_interval == 'week':
            active_newsletter = WeeklyNewsletter()
            self.add_weekly_newsletter(active_newsletter)
        else:
            active_newsletter = MonthlyNewsletter()
            self.add_monthly_newsletter(active_newsletter)


    def update_newsletter(self):
        global active_newsletter
        global subscriber_newsletter
        global subscribe_form_settings

        subscriber_newsletter.refresh_from_db()
        subscribe_form_settings.refresh_from_db()

        if not active_newsletter == None:
            self.remove_newsletter(active_newsletter)

        # Don't start if subscriber newsletter is turned off
        if subscribe_form_settings.show_form:
            self.add_newsletter()


newsletter_scheduler = BackgroundNewsletterScheduler()
