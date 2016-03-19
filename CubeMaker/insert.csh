#! /bin/csh -f

if ($#argv != 2) then
    echo "usage: insert <dir> <insertion-point>"
    exit(1)
endif
set outdir = $argv[1]
set ipoint = $argv[2]

cd $outdir

echo "inserting" $ipoint

foreach f ( `ls | sort -n -r` )
    set result = `echo $f $ipoint | awk '{ if ($1 >= $2) { print "yes"; } else { print "no"; }}'`
    if ($result == "yes") then
	set target = `echo $f | awk '{print $1 + 1}'`
	echo "DO   mv $f $target"
	if (-f $target) then
	    echo "abort: target exists!"
	    echo $target
	    exit(1)
	endif
	mv $f $target
    else
	echo "DONT mv $f"
    endif
end
exit(0)











