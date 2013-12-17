import webapp2
import re

form_signup="""
<!doctype = html>
 <html>
  <head>
   <style type="text/css">
    .label {text-align:right; color:navy;font-family:calibri,arial,sans-serif}
    .error {color:red}
   </style>
   <title>Unit 2 SignUp - erpreciso challenge
   </title>
  </head>
  <body>
   <h2>Signup</h2>
    <form method="post">
    
     <table>
     
      <tr>
       <td class="label">
		Username
       </td>
       <td>
        <input type="text" name="username" value="%(username)s">
       </td>
       <td class="error">
        %(username_error)s
       </td>
      </tr>
      
      <tr>
       <td class="label">
		Password
       </td>
       <td>
        <input type="password" name="password">
       </td>
       <td class="error">
        %(password_missing_error)s
       </td>
      </tr>
      
      <tr>
       <td class="label">
        Verify Password
       </td>
       <td>
        <input type="password" name="verify">
       </td>
       <td class="error">
        %(password_match_error)s
       </td>
      </tr>
      
      <tr>
       <td class="label">
		Email (optional)
       </td>
       <td>
        <input type="text" name="email" value="%(email)s">
       </td>
       <td class="error">
       %(mail_error)s
       </td>
      </tr>
      
      <tr>
       <td>
        <input type="submit">
       </td>
      </tr>
      
     </table>
    </form>
   </body/
 </html>
"""

form_rot13 = """
    <head>
      <style>
         body {color: black; font-family: calibri, arial, sans-serif}
      </style>
      <title>Unit 2 Rot 13 - erpreciso challenge
      </title>
    </head>
    <form method="post">
	<h2>Enter some text to ROT13:</h2>
	    <textarea name = "text" style="height: 100px; width: 400px;">%(contenuto)s</textarea>
	<br>
	<input type="Submit">
    </form>
    """

class SignupClass(webapp2.RequestHandler):
    
	def scrivi_signup(self,username="",email="",username_error_sw=False,password_missing_error_sw=False,password_match_error_sw=False,mail_error_sw=False):
		
		if username_error_sw:
			username_error="That's not a valid username."
		else:
			username_error=""
		if password_missing_error_sw:
			password_missing_error="That wasn't a valid password."
		else:
			password_missing_error=""
		if password_match_error_sw:
			password_match_error="Your passwords didn't match."
		else:
			password_match_error=""
		if mail_error_sw:
			mail_error="That's not a valid email."
		else:
			mail_error=""
		
		self.response.out.write(form_signup % {"username":username,
												"email":email,
												"username_error":username_error,
												"password_missing_error":password_missing_error,
												"password_match_error":password_match_error,
												"mail_error":mail_error})

	def get(self):
		#self.response.headers['Content-Type'] = 'text/plain'
		self.scrivi_signup()

	def post(self):
		username=self.request.get("username")
		ck_username = username
		password=self.request.get("password")
		verify_password=self.request.get("verify")
		email=self.request.get("email")
		#self.response.headers['Content-Type'] = 'text/plain'
		
		#verifica presenza username
		username_error_sw = False
		if username == "":
			username_error_sw = True
		#verifica correttezza username
		username_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		if username_re.match(ck_username) == None:
			username_error_sw = True
		#verifica presenza password
		password_missing_error_sw = False
		if password == "":
			password_missing_error_sw = True
		#verifica correttezza password
		password_re = re.compile(r"^.{3,20}$")
		if password_re.match(password) == None:
			password_missing_error_sw = True
		#verifica consistenza password
		password_match_error_sw = False
		if password != verify_password:
			password_match_error_sw = True
		#verifica correttezza email
		mail_error_sw = False
		if email != "":
			mail_re=re.compile(r"^[\S]+@[\S]+\.[\S]+$")
			if mail_re.match(email) == None:
				mail_error_sw = True	
		
		if password_match_error_sw or username_error_sw or password_missing_error_sw or mail_error_sw == True:
			self.scrivi_signup(username,email,username_error_sw,password_missing_error_sw,password_match_error_sw,mail_error_sw)
		else:
			self.redirect("/welcome?username=" + username)
           
class WelcomeClass(webapp2.RequestHandler):
	def get(self):
		username=self.request.get("username")
		user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		if user_re.match(username) == None:
			self.redirect("/signup")
		self.response.out.write("<h1>Welcome, " + username + "!</h1>")
  
class Rot13Class(webapp2.RequestHandler):
    
    def scrivi_form(self,contenuto=""):
        self.response.out.write(form_rot13 % {"contenuto":contenuto})
	
    def get(self):
        self.scrivi_form()
		
    def post(self):
        q=self.request.get("text")
        alf_l = {'a':'n','b':'o','c':'p','d':'q','e':'r',
        'f':'s','g':'t','h':'u','i':'v','j':'w',
        'k':'x','l':'y','m':'z','n':'a','o':'b',
        'p':'c','q':'d','r':'e','s':'f','t':'g',
        'u':'h','v':'i','w':'j','x':'k','y':'l',
        'z':'m'}
        
        alf_u = {'A':'N','B':'O','C':'P','D':'Q','E':'R',
        'F':'S','G':'T','H':'U','I':'V','J':'W',
        'K':'X','L':'Y','M':'Z','N':'A','O':'B',
        'P':'C','Q':'D','R':'E','S':'F','T':'G',
        'U':'H','V':'I','W':'J','X':'K','Y':'L',
        'Z':'M'}		
        t=[]
        g = ''	
		
        for p in str(q):
            if p in alf_l:			
                t.append('{0}'.format(alf_l[p]))
            elif p in alf_u:
                t.append('{0}'.format(alf_u[p]))
            elif p == "/":
                t[len(t):] = "&#47;"
            elif p==">":
                t[len(t):] = "&gt;"
            elif p=="<":
                t[len(t):] = "&lt;"
            elif p=='"':
                t[len(t):] = "&quot;"
            elif p=="&":
                t[len(t):] = "&amp;"
            else:
                t.append(p)
        g = g.join(r for r in t)	
        self.scrivi_form(g)
		
app = webapp2.WSGIApplication([('/rot13',Rot13Class),("/signup",SignupClass),("/welcome",WelcomeClass)], debug=True)
