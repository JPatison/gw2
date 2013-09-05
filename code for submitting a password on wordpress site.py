import mechanize
br = mechanize.Browser()

br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
response = br.open('http://vp-creations.com/?page_id=174')
#print response.read()
'''
for form in br.forms():
    print "Form name:", form.name
    print form
'''
br.form = list(br.forms())[1]

'''
for control in br.form.controls:
    print control
    print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
'''    
br['post_password']='vander'
response = br.submit()
html = response.read()

str(html)
print html

