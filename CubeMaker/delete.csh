#! /bin/csh -f

if ($#argv != 2) then
    echo "usage: delete <outdir> <delete-point>"
    exit(1)
endif
set outdir = $argv[1]
set dpoint = $argv[2]

cd $outdir

echo "deleting" $dpoint
rm -f $dpoint

foreach f ( `ls | sort -n` )
    set result = `echo $f $dpoint | awk '{ if ($1 > $2) { print "yes"; } else { print "no"; }}'`
    if ($result == "yes") then
	set target = `echo $f | awk '{print $1 - 1}'`
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



