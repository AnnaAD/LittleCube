#! /bin/csh -f

if ($#argv != 2) then
    echo "usage: generate <dir> <all or level number>"
    exit(1)
endif
set indir   = $argv[1]
set level   = $argv[2]

cd $indir

echo "    if (level == -2) {"
echo "        // left blank"

if ($level == "all") then
    set files = `ls | sort -n` 
else
    set files = $level
endif

foreach f ( $files )
    gawk -vlevel=$level -vn=$f -f ../generate.awk $f
end

echo "    }"
exit(0)














