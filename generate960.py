#!/usr/env python
# generate960.py - CLI script for generating 960gs custom grids(css)
# Copyright (C) 2010  Dejan Noveski <dr.mote@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
generate960.py - CLI script for generating custom 960gs grids (css)
Can generate grids will custom width/column number/gutter width.
Outputs to file or stdout

Usage:
    python generate960.py -h/--help

Requirements:
    jinja2
    argparse
"""

import argparse
import jinja2


#The template is added here so the script is self-contained
#Looks ugly, i know...
GRID_960 = """

/* Containers
---------------------------------------------------------------------*/
.container_{{column_number}} {
    margin-left: auto;
    margin-right: auto;
    width: {{column_number * column_width + column_number * gutter_width}}px;
    
    
}

/* Grid >> Children (Alpha ~ First, Omega ~ Last)
----------------------------------------------------------------------*/

.alpha {
    margin-left: 0 !important;
}

.omega {
        margin-right: 0 !important;
}

/* Grid >> Global
----------------------------------------------------------------------*/
{%for i in range(1, column_number+1) %} 
.grid_{{i}},{%endfor%}.grid_{{column_number}}{
    display:inline;
    float: left;
    position: relative;
    margin-left: {{gutter_width/2}}px;
    margin-right: {{gutter_width/2}}px;
}

/* Grid >> 2 Columns
----------------------------------------------------------------------*/
{%for i in range(1, column_number+1) %}
.container_{{column_number}} .grid_{{i}}{
    width:{{(i-1)* gutter_width + i * column_width}}px;
}
{%endfor%}

/* Prefix Extra Space >> 2 Columns
----------------------------------------------------------------------*/
{%for i in range(1, column_number+1) %}
    .container_{{ column_number }} .prefix_{{i}} {
    padding-left:{{i * gutter_width + i * column_width}}px;
}
{%endfor%}


/* Suffix Extra Space >> 2 Columns
----------------------------------------------------------------------*/
{%for i in range(1, column_number+1) %}
    .container_{{column_number}} .suffix_{{i}} {
    padding-right:{{i * gutter_width + i * column_width}}px;
}
{%endfor%}


/* Push Space >> 2 Columns
----------------------------------------------------------------------*/
{%for i in range(1, column_number+1) %}
    .container_{{column_number}} .push_{{i}} {
    left:{{i * gutter_width + i * column_width}}px;
}
{%endfor%}

/* Pull Space >> 2 Columns
----------------------------------------------------------------------*/
{%for i in range(1, column_number+1) %}
    .container_{{column_number}} .pull_{{i}} {
    right:{{ i * gutter_width + i * column_width}}px;
}
{%endfor%}

/* Clear Floated Elements
----------------------------------------------------------------------*/

.clear {
    clear: both;
    display: block;
    overflow: hidden;
    visibility: hidden;
    width: 0;
    height: 0;
}

.clearfix:after {
    clear: both;
    content: ' ';
    display: block;
    font-size: 0;
    line-height: 0;
    visibility: hidden;
    width: 0;
    height: 0;
}

.clearfix {
    display: inline-block;
}

* html .clearfix {
    height: 1%;
}

.clearfix {
    display: block;
}
"""




def generate_grid(width = 960, column_number = 12, gutter = 20):

    #Calculate the column width and render the template
    #This is the main logic :) thanks to Jinja2
    column_width = (width - column_number*gutter)/column_number
    template = jinja2.Template(GRID_960)
    return template.render(column_number = column_number,
            column_width = column_width, gutter_width = gutter)


if __name__ == "__main__":
    
    #argparse rocks! Setting up the arguments here
    parser = argparse.ArgumentParser(prog = "generate960",
            description = "Generates 960gs grids with output to file or cli",
            add_help = True)

    parser.add_argument("-w", "--width", action = "store", type = int,
            help = """Content width in px.Defaults to 960px.""",
            default = 960)
    parser.add_argument("-c", "--columns", action = "store", type = int,
            help = "Number of columns. Defaults to 12.", default = 12)
    parser.add_argument("-g", "--gutter", action = "store", type = int,
            help = """Gutter width in px. Defaults to 20px.""",
            default = 20)
    parser.add_argument("-f", "--file", action = "store", 
            help = """Name of the file to be saved. If this is not specified
            the css will be printed to stdout""")

    args = parser.parse_args()
    
    css = generate_grid(args.width, args.columns, args.gutter)
    if args.file:
        saved = open(args.file, 'w').write(css)
    else:
        print(css)
   
