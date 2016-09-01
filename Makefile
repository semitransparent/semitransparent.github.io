github:
	BASEDIR=$(CURDIR)
	INPUTDIR=$(BASEDIR)/content
	OUTPUTDIR=$(BASEDIR)/output

	ghp-import -b gh-pages -n $(OUTPUTDIR)
	git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git gh-pages
