# awk

BEGIN {
    if (level == "all") {
	printf("    } else if (level == %s) {\n", n);
    } else {
	printf("    } else if (level == 0) {\n");
    }
}

($1 == "__text__") {
    split($0, x, "__text__ ");
    printf("        levelTxt = \"%s\";\n", x[2]);
}

($1 == "__box__") {
    x1   = $2;
    y1   = $3;
    x2   = $4;
    y2   = $5;
    mode = $6;
    printf("        boxes.push({x:%d, y:%d, width:%d, height:%d, mode:%d});\n", x1, y1, x2-x1, y2-y1, mode);
}

