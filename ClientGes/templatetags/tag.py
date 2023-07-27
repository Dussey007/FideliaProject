from django import template
from urllib.parse import urlencode


register = template.Library()

@register.simple_tag
def url_replace (request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()






# from django import template

# register = template.Library()




# @register.simple_tag(takes_context = True)
# def param_replace(context, **kwargs):
#     d = context['request'].GET.copy()
#     for k, v in kwargs.items():
#         d[k] = v
#     for k in [k for k, v in d.items() if not v]:
#         del d[k]
#     return d.urlencode()



















