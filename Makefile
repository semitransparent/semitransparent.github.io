github:
	pelican content
	ghp-import -b gh-pages -n output
	git push -fq https://${GH_TOKEN}@github.com/$(TRAVIS_REPO_SLUG).git gh-pages
