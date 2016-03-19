    if (level == -2) {
        // left blank
    } else if (level == 0) {
        levelTxt = "Sometimes life is easy. Just run to the right!";
    } else if (level == 1) {
        levelTxt = "Life gives you barriers. So make jump-ade!";
        boxes.push({x:263, y:162, width:18, height:58, mode:0});
    } else if (level == 2) {
        levelTxt = "One little jump can lead to another?";
        boxes.push({x:277, y:86, width:18, height:134, mode:0});
        boxes.push({x:170, y:152, width:18, height:68, mode:0});
        boxes.push({x:389, y:150, width:17, height:70, mode:0});
    } else if (level == 3) {
        levelTxt = "But watch out! Death looms, in the lava pits...";
        boxes.push({x:237, y:206, width:87, height:23, mode:1});
    } else if (level == 4) {
        levelTxt = "Empty";
    }
