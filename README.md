Dash - a customized homepage of news and events
====

http://dashapp.herokuapp.com


This app relies on the WordNet corpora of NLTK, which cannot be installed non-locally:
https://groups.google.com/forum/?fromgroups=#!topic/nltk-users/D_nvJG8n4gM


Things that are wrong:
 - CSS orders items incorrectly in columns; should use horizontal box layout
 - News/Event icons do not appear on item corners (CSS display issue)
 - Django/Python/Heroku do not play well with unicode text

Things that work but need fixing:
 - Not built for speed/efficiency; querying of content APIs occurs on every page load
 - No 404/500 pages; debug is on
 - No validation/parameterization of user interests
 - Links to external sites; originally used Readability and on-site lightboxes, but API was blocked

Things that could be better:
 - Error checking is almost nonexistent; hasn't been stress tested
 - URL patterns could have been organized better
 - User interest sets are stored as single UserProfile fields; should be ManyToMany with users
 - Creates a custom UserProfile instead of a custom User model (not supported in Django 1.5)

...not an exhaustive list!
