#! /bin/csh -f

awk -f insert.awk CubeMaker/levels.js index.js                > index-new.js
m4 -DDEF_ONPHONE=true  index.pre index-new.js index.post      > index.html
m4 -DDEF_ONPHONE=false index.pre index-new.js index.post-test > index-test.html


