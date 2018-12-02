from django import template

register = template.Library()

@register.filter(name='index')
def indexThis(List, i):
    return List[int(i)]

@register.filter(name='indexLower')
def indexThisOneLower(List, i):
    return List[int(i-1)]


@register.filter(name="onelower")
def makeOneLower(inputNum):
    return inputNum - 1