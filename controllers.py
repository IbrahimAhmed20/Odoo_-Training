# Answer of Q(15) Explain the core difference between the QWeb directives t-out (or t-esc)
#and the deprecated t-raw in terms of security when displaying data
#originating from the database

#The difference is in HTML (code) parsing or not. When you use t-esc it will literally print out the value from the field you want to print. 
#When you use t-raw in combination with an HTML field for example it will keep the content in HTML. 
#If you would do a t-esc on an HTML field it will print your HTML code without interpreting it to actual code.
#For example you have a field with: <p>My code</p>
#If you would use t-raw it will be handled as HTML and so your <p> element won't be shown because it is converted. 
#When you would do the same with t-esc it would literally print <p>My code</p> on your report.