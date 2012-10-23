from main import *

def age_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))

def age_get(key):
    r = memcache.get(key)
    if r:
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val, age = None, 0
    return val, age

def add_post(ip, post):
    post.put()
    get_posts(update = True)
    return str(post.key().id())

def get_posts(update = False):
    q = Post.all().order('-created').fetch(limit = 10)
    mc_key = 'BLOGS'
    posts, age = age_get(mc_key)
    if update or posts is None:
        posts = list(q)
        age_set(mc_key, posts)
    return posts, age

def age_str(age):
    s = 'queried %s seconds ago'
    age = int(age)
    if age == 1:
        s = s.replace('seconds', 'second')
    return s % age

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)    
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)	

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.last_modified.strftime(time_fmt)}
        return d

class FrontPageHandler(BaseHandler):
    def get(self):
        if not self.user:
           self.redirect('/login')	
        posts, age = get_posts()
        if self.format == 'html':
            self.render('frontpage.html', posts = posts,
                        age = age_str(age))
        elif self.format == 'json':
            return self.render_json([p.as_dict() for p in posts])

class PostPage(BaseHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id
        post, age = age_get(post, key)
        if not post:
            key = db.Key.from_path('Post', int(post_id),
                                   parent = blog_key())
            post = db.get(key)
            age_set(post_key, post)
            age = 0
        if self.format == 'html':
            self.render("permalink.html", post = post, age = age_str(age))
        elif format == 'json':
            self.render_json(post.as_dict())

class NewPostHandler(BaseHandler):
	def get(self):
		self.render("newpost.html")

	def post(self):
		subject = self.request.get('subject')
		content = self.request.get('content')

		if subject and content:
			p = Post(parent = blog_key(), subject = subject, content = content)
			p.put()
			self.redirect('/blog/%s' % str(p.key().id()))
		else:
			error = """
Please enter subject and content before creating a blog post!
"""
			self.render("newpost.html", subject = subject,
						content = content, error = error)
    
app = webapp2.WSGIApplication([('/blog/?(?:.json)?', FrontPageHandler),
							   ('/blog/([0-9]+)(?:.json)?', PostPage),
							   ('/blog/newpost', NewPostHandler)
							  ],
							  debug=True)
