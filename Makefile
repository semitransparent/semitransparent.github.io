BASEDIR=$(TRAVIS_BUILD_DIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output

publish:
	ls $(INPUTDIR)
	pelican $(INPUTDIR)

github:
	ghp-import -b master -n $(OUTPUTDIR)
	git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git master
