TAG = PR1
git for-each-ref refs/tags/$TAG --shell --format='
TAG=%(refname)
TYPE=%(objecttype)
COMMIT=%(objectname)
TAGGER=%(tagger)
EMAIL=%(taggeremail)
DATE=%(taggerdate)
CONTENTS=%(contents)
'
