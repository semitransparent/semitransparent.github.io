BASEDIR=$(TRAVIS_BUILD_DIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output

publish:
	ls $(INPUTDIR)
	pelican -D $(INPUTDIR)

github:
	ghp-import -b gh-pages -n content
	git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git gh-pages
