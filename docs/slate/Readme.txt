This is the slate build for the HPE RESTful Interface Tool Documentation website.
========================================
It's based on Slate.

run these commands locally (in this folder) to start:
bundle install
bundle exec middleman server

Note: There may be some dependencies that your Ruby needs to download. This is supported in Linux or OS X.
Windows may work, but is unsupported. 

You can now see the docs at:

http://localhost:4567

Building the Website
=========================
run in this directory:
bundle exec middleman build --clean

This creates a folder named "build" with the static HTML files that need to be uploaded.

Structure of Docs
=========================
Everything is written in Markdown.

index.html.md is the CORE file. Everything else is written and placed in the "includes" folder.

The order shown in the "includes:" subheader is the order the pages are inserted.

# Header 1
## Header 2
### Header 3
#### Header 4

Headers 1-4 are divided on the left's Table of Contents for ease of locating. 

All new markdown files MUST have an underscore. i.e. "_example.md". In the index.html.md this is referenced:
- example

Note: the underscore is not included when listing it in the index.html.md file.

A markdown file DOES NOT have to begin with Header 1. If it starts with a subheader,
it will be loaded into the last section found.

Formatting Codeblocks
=========================
For these docs, use ```code here```, instead of:
```shell
code here
```

Some of our commands don't do very well with the Shell auto-highlighting/formatting.

Aside tags
=========================
Aside tags can be used for info, notice, warning (classes). 
Also, note that within the tag, it becomes HTML, and no longer markdown, so use <b></b> to bold, etc.

Customization
==========================
Basic changes to sizes, padding and colors are in 'variables.scss' in the stylesheets folder.

Other places to make changes are:
'screen.css.scss'
'print.css.scss'

Uploading to Github Pages
==========================
Put the files from the 'build' folder into the gh-pages branch in the hprest repo. Make sure the main page is called index.html!

Uploading to Your Own Server
=============================
bundle exec middleman build --clean

Slate Documentation Links
==========================
https://github.com/lord/slate/wiki