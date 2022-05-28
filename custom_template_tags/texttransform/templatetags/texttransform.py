from lxml.html import fromstring
from lxml.html.clean import Cleaner
from collections import Iterable
from django import template
from django.utils.safestring import mark_safe
from django.utils.text import normalize_newlines

register = template.Library()

# Adapted from (https://stackoverflow.com/questions/2165943/removing-html-tags-from-a-text-using-regular-expression-in-python)

@register.filter
def remove_headers(html):
    try: # Fails when no html
        doc = fromstring(html)

        tags = [ 'h1','h2','h3','h4','h5','h6' ]
        args = {'meta':False, 'safe_attrs_only':False, 'page_structure':False,
                    'scripts':True, 'style':True, 'links':True, 'remove_tags':tags}

        cleaner = Cleaner(**args)

        return cleaner.clean_html(doc).text_content()
    except:
        return html


@register.filter
def remove_p_tags(html):
    try:
        doc = fromstring(html)

        tags = [ 'p' ]
        args = {'meta':False, 'safe_attrs_only':False, 'page_structure':False,
                'scripts':True, 'style':True, 'links':True, 'remove_tags':tags}

        cleaner = Cleaner(**args)

        return cleaner.clean_html(doc).text_content()
    except:
        return html


@register.filter
def remove_newlines(text, replacement=' '):
    """
    Removes and replaces all newline characters from a block of text.
    default replacement=' '

    from https://www.otcollect.com/collection/django/page/akMRZ9LMDRzsbkwzCSS5/django-filter-tag-to-remove-new-lines
    """
    try:
        # Normalize new lines
        normalized_text = normalize_newlines(text)
        # Replace newlines with replacement
        return mark_safe(normalized_text.replace('\n', replacement))
    except:
        return text


@register.filter
def truncate_uniform_ljust(text, n):
    try:
        n = int(n)
        if len(text) > n:
            return (text[:(n-3)] + '...').ljust(n)
        else:
            return text[:n].ljust(n)
    except:
        return text


@register.filter
def truncate_uniform_rjust(text, n):
    n = int(n)
    if len(text) > n:
        return (text[:(n-3)] + '...').rjust(n)
    else:
        return text[:n].rjust(n)


@register.simple_tag
def try_eval_text(text):
    try:
        result = eval(text)
        return result
    except:
        return text


@register.simple_tag
def is_iterable(obj):
    return isinstance(obj, Iterable)


@register.simple_tag
def is_dict(obj):
    return isinstance(obj, dict)
