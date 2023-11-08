from django import template
from django.utils.translation import gettext


register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    # print ("request", request, type(request))
    dict_ = request.GET.copy()
    # print ("url_replace")
    # print ("dict_", dict_, field, value )

    dict_[field] = value
    return dict_.urlencode()


@register.simple_tag
def set_mem(mem_name, mem_add):
    if type(mem_name) == int and type(mem_add) == int:
        mem_name = mem_name + mem_add
    else:
        mem_name = 0
    return (mem_name)


@register.simple_tag
def set_mem_date(mem_name, mem_add):
    mem_name = mem_add
    return (mem_name)


@register.simple_tag
def set_int_separate(mem_int):
    m_return = '{0:,}'.format(mem_int)
    return (m_return)


@register.filter
def get_values_from_date(dictionary, key):
    # special filter for cabb_users.html
    str_date = key.split(' ')[0]
    vals = dictionary.get(str_date)
    if vals:
        joined = vals.get('joined', '')
        played = vals.get('played', '')
        tickets = vals.get('tickets', '')
        return f"{str_date},  {gettext('users')} {joined}, {gettext('Players')} {played}, {gettext('tickets')} {tickets}"
    else:
        return ''
