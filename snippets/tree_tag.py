# !title: Tree template tag
# !date: 2012-07-12
# !tags: Django
# !author: Mike Yumatov

from django import template


register = template.Library()


class TreeByLevelNode(template.Node):

    def __init__(self, obj_name, level_name, nodelist_header,
                 nodelist_leaf_top, nodelist_leaf_bottom, nodelist_footer):
        self.obj = template.Variable(obj_name)
        self.level_name = level_name
        self.nodelist_header = nodelist_header
        self.nodelist_leaf_top = nodelist_leaf_top
        self.nodelist_leaf_bottom = nodelist_leaf_bottom
        self.nodelist_footer = nodelist_footer

    def render(self, context):
        if 'tree' in context:
            parenttree = context['tree']
        else:
            parenttree = {}
        context.push()
        try:
            obj = self.obj.resolve(context)
        except template.VariableDoesNotExist:
            obj = []
        nodelist = template.NodeList()
        level = 0
        tree_dict = context['tree'] = {'parenttree': parenttree}
        for item in obj:
            new_level = self.get_level(item)
            if new_level is None:
                continue
            tree_dict['level'] = new_level
            tree_dict['leaf'] = item
            if new_level > level:
                for i in range(new_level - level):
                    for node in self.nodelist_header:
                        nodelist.append(node.render(context))
            elif new_level < level:
                for i in range(level - new_level):
                    for node in self.nodelist_leaf_bottom:
                        nodelist.append(node.render(context))
                    for node in self.nodelist_footer:
                        nodelist.append(node.render(context))
                for node in self.nodelist_leaf_bottom:
                    nodelist.append(node.render(context))
            else:
                for node in self.nodelist_leaf_bottom:
                    nodelist.append(node.render(context))
            level = new_level
            for node in self.nodelist_leaf_top:
                nodelist.append(node.render(context))
        for i in range(level):
            for node in self.nodelist_leaf_bottom:
                nodelist.append(node.render(context))
            for node in self.nodelist_footer:
                nodelist.append(node.render(context))
        context.pop()
        return nodelist.render(context)

    def get_level(self, obj):
        try:
            level = obj[self.level_name]
        except (KeyError, TypeError):
            try:
                level = getattr(obj, self.level_name)
            except AttributeError:
                return None
        try:
            return level()
        except TypeError:
            return level


TREE_TYPE_LIST = {'level': TreeByLevelNode}


@register.tag
def tree(parser, token):
    bits = token.contents.split()
    if len(bits) != 6 or bits[2] != 'with' or bits[4] != 'as' or \
       bits[5] not in TREE_TYPE_LIST.keys():
        raise template.TemplateSyntaxError(
            '%r: wrong formatted argument list' % bits[0])
    nodelist_header = parser.parse(('leaf',))
    token = parser.next_token()
    nodelist_leaf_top = parser.parse(('subtree',))
    token = parser.next_token()
    nodelist_leaf_bottom = parser.parse(('endleaf',))
    token = parser.next_token()
    nodelist_footer = parser.parse(('endtree',))
    parser.delete_first_token()
    return TREE_TYPE_LIST[bits[5]](
        bits[1], bits[3], nodelist_header, nodelist_leaf_top,
        nodelist_leaf_bottom, nodelist_footer)
