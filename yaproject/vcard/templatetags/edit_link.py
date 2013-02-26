from django import template
from django.core.urlresolvers import reverse


register = template.Library()


class EditLinkNode(template.Node):
    def __init__(self, target):
        self.target = template.Variable(target)

    def render(self, context):
        obj = self.target.resolve(context)
        pattern = 'admin:{0}_{1}_change'.format(obj._meta.app_label,
            obj._meta.module_name)
        return '<a href="{}">Edit(admin)</a>'.format(reverse(pattern,
        args=[obj.pk]))


def get_edit_link(parser, token):
    try:
        tag_name, target = token.split_contents()
    except ValueError:
        err = "%r tag requires only one arguments" % token.contents.split()[0]
        raise template.TemplateSyntaxError(err)
    return EditLinkNode(target)

register.tag('get_edit_link', get_edit_link)
