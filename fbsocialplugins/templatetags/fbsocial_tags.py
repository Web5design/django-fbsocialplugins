from django import template

register = template.Library()

def parse_arguments(string):
    """
    Accepts a string in this format:
    "arg1=val1, arg2=val2, arg3=val3"
    and returns something like this:
    {
        'arg1': 'val1',
        'arg2': 'val2',
        'arg3': 'val3',
    }
    """
    string = string.replace('"', '')
    
    arguments = string.split(',')
    pars = {}
    
    for arg in arguments:
        a = map(lambda x: x.strip(), arg.split('='))
        pars[a[0]] = a[1]
    
    print pars

    return pars

def check_arguments(token):
    bits = token.split_contents()[1:]
    
    if len(bits) < 1:
        raise template.TemplateSyntaxError, '%r tag requires at least one argument' % token.contents.split()[0]
    
    if len(bits) > 1:
        if not (bits[1].startswith('"') and bits[1].endswith('"')):
            raise template.TemplateSyntaxError, '%r second argument should be in quotes' % token.contents.split()[0]

    return bits

class LikeButtonNode(template.Node):
	template = ('<iframe src="http://www.facebook.com/plugins/like.php?href=%(url)s&amp;'
	'layout=%(layout)s&amp;width=%(width)s&amp;show_faces=%(show_faces)s&amp;'
	'action=%(action)s&amp;colorscheme=%(color_scheme)s&amp;font=%(font)s&amp;height=%(height)s" ' 
	'scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:%(width)spx; '
	'height:%(height)spx;" allowTransparency="true"></iframe>')

	def __init__(self, options):
		if (options.get('faces', 'false') == 'false'):
			options['height'] = '35'
		else:
			options['height'] = '80'
		
		self.options = options

	
	def render(self, context):
		return self.template % self.options

@register.tag(name="like_button")
def like_button(parser, token, no_var=False):
    """
    This will render facebook like button
    
    Usage::
    
    {% load fbsocial_tags %}
    {% like_button urlvar "args"  %}
    	
	Required argument:

	* href - the URL to like. The XFBML version defaults to the current page.
	
	Options:
	
	* layout - there are three options.
	* 1. standard - displays social text to the right of the button and friends' profile photos below. Minimum width: 225 pixels. Default width: 450 pixels. Height: 35 pixels (without photos) or 80 pixels (with photos).
	* 2. button_count - displays the total number of likes to the right of the button. Minimum width: 90 pixels. Default width: 90 pixels. Height: 20 pixels.
	* 3. box_count - displays the total number of likes above the button. Minimum width: 55 pixels. Default width: 55 pixels. Height: 65 pixels.
	* show_faces - specifies whether to display profile photos below the button (standard layout only)
	* width - the width of the Like button.
	* action - the verb to display on the button. Options: 'like', 'recommend'
	* font - the font to display in the button. Options: 'arial', 'lucida grande', 'segoe ui', 'tahoma', 'trebuchet ms', 'verdana'
	* colorscheme - the color scheme for the like button. Options: 'light', 'dark'
	* ref - a label for tracking referrals; must be less than 50 characters and can contain alphanumeric characters and some punctuation (currently +/=-.:_). The ref attribute causes two parameters to be added to the referrer URL when a user clicks a link from a stream story about a Like action:
	* 1. fb_ref - the ref parameter
	* 2. fb_source - the stream type ('home', 'profile', 'search', 'other') in which the click occurred and the story type ('oneline' or 'multiline'), concatenated with an underscore.

	
	"""
        
    bits = check_arguments(token)
    
    allowed_values = {
        'layout': ('standard', 'button_count'),
        'show_faces': ('true', 'false'),
        'action': ('like', 'recommend'),
        'font': ('arial', 'lucida grande', 'segoe ui', 'tahoma', 'trebuchet ms', 'verdana'),
        'color_scheme': ('light', 'dark'),
        'width': (200, ),
    }
    
    try:
        arguments = parse_arguments(bits[1])
    except IndexError:
        arguments = {}
    

    arguments['url'] = bits[0]
    
    for key, values in allowed_values.items():
        par = arguments.get(key, values[0])

        arguments[key] = par

    arguments['height'] = '35'
    if arguments['show_faces'] == 'true':
        arguments['height'] = '80'

    return LikeButtonNode(arguments)

