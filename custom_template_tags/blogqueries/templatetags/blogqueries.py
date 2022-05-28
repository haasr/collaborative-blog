from django import template
from admin_pages.models import Post

register = template.Library()

MONTHS_DICT = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}

@register.simple_tag
def count_posts_in_year(year):
    yr = Post.objects.filter(og_date__year=year, visibility='public')
    return len(yr)

@register.simple_tag
def count_posts_in_month(month, year):
    month_int = MONTHS_DICT[month.lower()]
    mo = Post.objects.filter(og_date__year=year, og_date__month=month_int, visibility='public')
    return len(mo)