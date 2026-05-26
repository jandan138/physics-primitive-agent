# Multi-venue LaTeX paper build system.
# Usage: make list | make accv | make arxiv | make eccv | make neurips | make all | make clean | make template-check | make check

VENUES := accv arxiv eccv neurips
SHARED_DIR := shared
SHARED_SRCS := $(shell find $(SHARED_DIR) -type f \( -name '*.tex' -o -name '*.bib' -o -name '*.cls' -o -name '*.sty' -o -name '*.pdf' -o -name '*.png' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.yaml' -o -name '*.yml' \) -print 2>/dev/null)

.PHONY: all clean list template-check check check-latex-tools check-external-class $(VENUES) $(addprefix clean-,$(VENUES)) $(addprefix check-template-,$(VENUES))

all: $(VENUES)

list:
	@printf 'Available venues: %s\n' '$(VENUES)'
	@printf 'Primary: accv\n'
	@printf 'Transfer candidates: arxiv eccv neurips\n'

template-check: check-latex-tools $(addprefix check-template-,$(VENUES))
	@echo 'Template check complete.'

check-latex-tools:
	@if ! command -v latexmk >/dev/null 2>&1; then \
		if ! command -v pdflatex >/dev/null 2>&1 || ! command -v bibtex >/dev/null 2>&1; then \
			echo 'Missing LaTeX build tooling: install latexmk, or install both pdflatex and bibtex for fallback.'; \
			exit 1; \
		fi; \
	fi

check-template-accv:
	@for file in accv.sty accvabbrv.sty llncs.cls splncs04.bst ACCV_TEMPLATE_LICENSE; do \
		if [ ! -f "venues/accv/$$file" ]; then \
			echo "Missing official ACCV template file: venues/accv/$$file"; \
			exit 1; \
		fi; \
	done

check-template-arxiv:
	@true

check-template-eccv:
	@cls='eccv.sty'; local='venues/eccv/eccv.sty'; \
	if [ -f "$$local" ]; then exit 0; fi; \
	if command -v kpsewhich >/dev/null 2>&1 && kpsewhich "$$cls" >/dev/null 2>&1; then exit 0; fi; \
	echo "Missing $$cls for eccv. Install the ECCV author kit or commit $$local."; \
	exit 1

check-template-neurips:
	@if [ ! -f venues/neurips/neurips_2026.sty ]; then \
		echo 'Missing NeurIPS style: expected venues/neurips/neurips_2026.sty'; \
		exit 1; \
	fi

check-external-class:
	@cls='$(CLASS)'; venue='$(VENUE)'; local="venues/$(VENUE)/$(CLASS)"; \
	if [ -f "$$local" ]; then exit 0; fi; \
	if command -v kpsewhich >/dev/null 2>&1 && kpsewhich "$$cls" >/dev/null 2>&1; then \
		exit 0; \
	fi; \
	if command -v pdflatex >/dev/null 2>&1; then \
		mkdir -p "venues/$$venue/build/template-check"; \
		class_name=`basename "$$cls" .cls`; \
		printf '\\documentclass{%s}\n\\begin{document}x\\end{document}\n' "$$class_name" > "venues/$$venue/build/template-check/check.tex"; \
		if cd "venues/$$venue" && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build/template-check build/template-check/check.tex >/dev/null 2>&1; then \
			exit 0; \
		fi; \
	fi; \
	echo "Missing $$cls for $$venue. Install the TeX Live package or commit $$local."; \
	exit 1

define VENUE_RULE
$(1)_MAIN := venues/$(1)/main.tex
$(1)_LOCAL := $(shell find venues/$(1) -type f \( -name '*.tex' -o -name '*.sty' -o -name '*.cls' -o -name '*.bib' -o -name '.latexmkrc' -o -name 'STATUS.md' \) -print 2>/dev/null)
$(1)_PDF := venues/$(1)/build/main.pdf
$(1)_BUILDDIR := venues/$(1)/build

$$($(1)_PDF): $$($(1)_MAIN) $$($(1)_LOCAL) $(SHARED_SRCS) | $$($(1)_BUILDDIR)
	@$$(MAKE) check-latex-tools
	@$$(MAKE) check-template-$(1)
	@if command -v latexmk >/dev/null 2>&1; then \
		cd venues/$(1) && latexmk -cd -pdf -outdir=build -interaction=nonstopmode -halt-on-error main.tex; \
	else \
		cd venues/$(1) && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex && BIBINPUTS="$$(pwd)/../../shared:" bibtex build/main && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex && pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex; \
	fi

$$($(1)_BUILDDIR):
	@mkdir -p $$@

$(1): $$($(1)_PDF)
	@echo '=== $(1) built: $$($(1)_PDF) ==='

clean-$(1):
	@cd venues/$(1) && latexmk -C -outdir=build 2>/dev/null || true
	@rm -rf $$($(1)_BUILDDIR)
endef

$(foreach v,$(VENUES),$(eval $(call VENUE_RULE,$(v))))

clean: $(addprefix clean-,$(VENUES))
	@rm -rf submissions arxiv-submission camera-ready

check:
	@for venue in $(VENUES); do \
		echo "=== $$venue page/word diagnostics ==="; \
		texcount -inc -total "venues/$$venue/main.tex" 2>/dev/null || echo 'texcount not installed'; \
		echo ''; \
	done
