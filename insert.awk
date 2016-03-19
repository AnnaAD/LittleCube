# awk

BEGIN {
    # print "MODE", 0;
    mode = 0;
    cnt = 0;
}

($2 == "BEGIN") {
    # print "MODE", 1;
    mode = 1;
}

(mode == 1) {
    print $0;
}

($2 == "INSERT_LEVELS") {
    for (i = 0; i < cnt; i++) {
	print line[i];
    }
}

(mode == 0) {
    line[cnt] = $0;
    # print "RECORD", cnt, line[cnt];
    cnt += 1;
}

