clean:
	rm -rf output

html:
	snippets -t theme

output/CNAME:
	cp CNAME output/CNAME

deploy: html output/CNAME
	ghp-import output
	git push origin gh-pages

.PHONY: clean html deploy
