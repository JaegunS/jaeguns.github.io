# default target
all: pdf

# generate resume PDF from clean markdown
pdf: resume.md build_resume.py
	python build_resume.py
	@echo "generated resume.pdf"

# clean generated files
clean:
	rm -f resume.pdf resume.tex
	rm -f *.aux *.log *.out
	@echo "cleaned build artifacts"
