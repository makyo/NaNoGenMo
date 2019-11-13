.PHONY: help
help: ## This help.
	@# This is ugly as hell and I hate awk
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: final
final: reset toc ## full document of the book for final print

.PHONY: proof
proof: engage-letter engage-frame engage-draft toc reset ## full proof document of the book with frames and watermark

.PHONY: draft
draft: engage-draft toc reset ## draft document of thebook with watermark

.PHONY: plain
plain: ## full document of the book with no proofing marks
	xelatex book.tex

.PHONY: toc
toc: plain ## full book with ToC re-rendering in case of page changes
	xelatex book.tex

.PHONY: ebook
ebook: ## render ePub file from LaTeX
	pandoc book.tex -o ebooks/book.epub -t epub3 --wrap=none

.PHONY: frame
engage-frame: ## turn on frame marking
	cp includes/_frame.tex includes/frame.tex

.PHONY: engage-letter
engage-letter: ## force letter paper
	echo '\input{includes/_geometry-letter.tex}' > includes/geometry.tex

.PHONY: draft
engage-draft: ## turn on draft watermark
	cp includes/_draft.tex includes/draft.tex

.PHONY: reset
reset: ## reset frame marking, draft watermark, and letter paper
	echo '%' > includes/draft.tex
	echo '%' > includes/frame.tex
	echo '\input{includes/_geometry-trade.tex}' > includes/geometry.tex

.PHONY: content
content: ## build the markdown content into LaTeX
	for in in src/content/*.md; do \
		out=`echo $$in | sed -e 's/\.md/.tex/' | sed -e 's/.*\///'`; \
		echo "$$in => $$out"; \
		pandoc -f markdown -t latex--wrap=none --top-level-division=chapter -o content/$$out $$in ; \
	done
