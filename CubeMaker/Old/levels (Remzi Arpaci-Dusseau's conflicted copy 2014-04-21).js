    if (level == -2) {
        // left blank
    } else if (level == 0) {
        levelTxt = "Just run to the right, silly cube!";
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
        boxes.push({x:191, y:217, width:91, height:10, mode:1});
    } else if (level == 4) {
        levelTxt = "Use bouncy pads for super jumps!";
        boxes.push({x:261, y:80, width:29, height:145, mode:0});
        boxes.push({x:127, y:218, width:107, height:5, mode:2});
    } else if (level == 5) {
        levelTxt = "Little cube it is time for me to depart...";
        boxes.push({x:112, y:150, width:77, height:22, mode:0});
        boxes.push({x:236, y:79, width:79, height:21, mode:0});
        boxes.push({x:549, y:2, width:19, height:138, mode:0});
        boxes.push({x:381, y:146, width:137, height:22, mode:0});
        boxes.push({x:116, y:211, width:419, height:12, mode:1});
        boxes.push({x:382, y:90, width:138, height:2, mode:0});
    } else if (level == 6) {
        levelTxt = "Keep your sights sharp.";
        boxes.push({x:139, y:156, width:38, height:66, mode:0});
        boxes.push({x:232, y:108, width:98, height:31, mode:0});
        boxes.push({x:392, y:205, width:176, height:18, mode:1});
        boxes.push({x:464, y:91, width:2, height:2, mode:0});
    } else if (level == 7) {
        levelTxt = "Your hopes high.";
        boxes.push({x:187, y:182, width:15, height:40, mode:0});
        boxes.push({x:247, y:126, width:19, height:95, mode:0});
        boxes.push({x:291, y:38, width:3, height:184, mode:0});
        boxes.push({x:295, y:213, width:273, height:7, mode:1});
        boxes.push({x:402, y:120, width:71, height:10, mode:0});
        boxes.push({x:276, y:75, width:16, height:8, mode:0});
        boxes.push({x:265, y:173, width:7, height:3, mode:0});
    } else if (level == 8) {
        levelTxt = "And don't let anyone bring you down.";
        boxes.push({x:104, y:216, width:392, height:9, mode:1});
        boxes.push({x:145, y:174, width:39, height:8, mode:0});
        boxes.push({x:216, y:134, width:41, height:8, mode:0});
        boxes.push({x:304, y:78, width:54, height:9, mode:0});
    } else if (level == 9) {
        levelTxt = "Good bye.";
    } else if (level == 10) {
        levelTxt = "";
        boxes.push({x:137, y:208, width:24, height:14, mode:1});
        boxes.push({x:186, y:209, width:21, height:12, mode:1});
        boxes.push({x:231, y:204, width:18, height:16, mode:1});
        boxes.push({x:276, y:196, width:23, height:24, mode:1});
    } else if (level == 11) {
        levelTxt = "Hey, Little Cube! What are you doing here?";
        boxes.push({x:154, y:181, width:5, height:43, mode:0});
        boxes.push({x:207, y:150, width:6, height:81, mode:0});
        boxes.push({x:254, y:114, width:7, height:112, mode:0});
        boxes.push({x:306, y:85, width:9, height:137, mode:0});
        boxes.push({x:159, y:218, width:48, height:9, mode:1});
        boxes.push({x:214, y:220, width:40, height:8, mode:1});
        boxes.push({x:263, y:219, width:43, height:9, mode:1});
    } else if (level == 12) {
        levelTxt = "You can't be here!";
        boxes.push({x:136, y:219, width:58, height:7, mode:2});
        boxes.push({x:260, y:218, width:59, height:8, mode:2});
        boxes.push({x:391, y:218, width:56, height:11, mode:2});
        boxes.push({x:22, y:87, width:545, height:13, mode:1});
    } else if (level == 13) {
        levelTxt = "You can't jump far enough!";
        boxes.push({x:188, y:219, width:145, height:8, mode:1});
    } else if (level == 14) {
        levelTxt = "You aren't smart enough!";
        boxes.push({x:157, y:164, width:23, height:63, mode:0});
        boxes.push({x:244, y:133, width:23, height:93, mode:0});
        boxes.push({x:333, y:100, width:20, height:124, mode:0});
        boxes.push({x:381, y:31, width:187, height:9, mode:0});
        boxes.push({x:355, y:218, width:212, height:13, mode:1});
        boxes.push({x:269, y:218, width:64, height:13, mode:1});
        boxes.push({x:182, y:220, width:63, height:11, mode:1});
        boxes.push({x:490, y:186, width:35, height:14, mode:0});
        boxes.push({x:361, y:65, width:15, height:11, mode:0});
        boxes.push({x:380, y:2, width:9, height:38, mode:0});
    } else if (level == 15) {
        levelTxt = "You'll get hurt...";
        boxes.push({x:140, y:153, width:14, height:67, mode:1});
        boxes.push({x:184, y:172, width:12, height:48, mode:1});
        boxes.push({x:228, y:151, width:13, height:69, mode:1});
        boxes.push({x:267, y:169, width:11, height:51, mode:1});
        boxes.push({x:305, y:150, width:12, height:71, mode:1});
        boxes.push({x:346, y:218, width:144, height:12, mode:1});
    } else if (level == 16) {
        levelTxt = "I'm just worried about you. That's all...";
        boxes.push({x:119, y:183, width:21, height:45, mode:0});
        boxes.push({x:198, y:163, width:22, height:65, mode:0});
        boxes.push({x:279, y:135, width:6, height:7, mode:0});
        boxes.push({x:355, y:172, width:7, height:9, mode:0});
        boxes.push({x:417, y:87, width:8, height:8, mode:0});
        boxes.push({x:482, y:168, width:7, height:8, mode:0});
        boxes.push({x:520, y:40, width:10, height:9, mode:0});
        boxes.push({x:554, y:88, width:14, height:188, mode:0});
        boxes.push({x:220, y:216, width:334, height:19, mode:1});
        boxes.push({x:140, y:217, width:58, height:20, mode:1});
    } else if (level == 17) {
        levelTxt = "You should leave. Now.";
        boxes.push({x:166, y:155, width:12, height:65, mode:1});
        boxes.push({x:207, y:156, width:11, height:64, mode:1});
        boxes.push({x:246, y:161, width:10, height:59, mode:1});
        boxes.push({x:285, y:173, width:7, height:47, mode:1});
        boxes.push({x:320, y:166, width:10, height:54, mode:1});
        boxes.push({x:355, y:148, width:9, height:72, mode:1});
    } else if (level == 18) {
        levelTxt = "What you can't see can't hurt you, right?";
        boxes.push({x:57, y:198, width:2, height:2, mode:1});
        boxes.push({x:68, y:207, width:3, height:2, mode:1});
        boxes.push({x:67, y:162, width:2, height:3, mode:1});
        boxes.push({x:83, y:184, width:2, height:2, mode:1});
        boxes.push({x:81, y:119, width:3, height:3, mode:1});
        boxes.push({x:111, y:188, width:1, height:2, mode:1});
        boxes.push({x:115, y:152, width:2, height:2, mode:1});
        boxes.push({x:123, y:86, width:3, height:2, mode:1});
        boxes.push({x:136, y:205, width:2, height:2, mode:1});
        boxes.push({x:151, y:174, width:24, height:3, mode:1});
        boxes.push({x:161, y:127, width:3, height:4, mode:0});
        boxes.push({x:241, y:179, width:3, height:4, mode:0});
        boxes.push({x:314, y:142, width:3, height:3, mode:0});
        boxes.push({x:200, y:200, width:85, height:2, mode:1});
        boxes.push({x:206, y:134, width:4, height:3, mode:1});
        boxes.push({x:187, y:100, width:4, height:5, mode:1});
        boxes.push({x:261, y:136, width:3, height:2, mode:1});
        boxes.push({x:337, y:183, width:2, height:4, mode:1});
        boxes.push({x:343, y:105, width:3, height:56, mode:1});
        boxes.push({x:337, y:48, width:13, height:2, mode:0});
        boxes.push({x:288, y:36, width:21, height:28, mode:1});
        boxes.push({x:359, y:213, width:4, height:4, mode:1});
        boxes.push({x:535, y:218, width:33, height:2, mode:1});
        boxes.push({x:373, y:84, width:9, height:4, mode:1});
        boxes.push({x:378, y:177, width:6, height:6, mode:1});
        boxes.push({x:412, y:215, width:7, height:5, mode:1});
        boxes.push({x:420, y:178, width:4, height:2, mode:1});
        boxes.push({x:440, y:214, width:3, height:2, mode:1});
        boxes.push({x:457, y:192, width:5, height:3, mode:1});
        boxes.push({x:392, y:122, width:14, height:2, mode:0});
        boxes.push({x:230, y:86, width:4, height:3, mode:1});
        boxes.push({x:155, y:160, width:2, height:3, mode:0});
        boxes.push({x:448, y:51, width:5, height:4, mode:0});
        boxes.push({x:408, y:32, width:4, height:5, mode:1});
        boxes.push({x:439, y:98, width:3, height:2, mode:1});
        boxes.push({x:488, y:198, width:3, height:22, mode:1});
        boxes.push({x:446, y:138, width:11, height:4, mode:1});
        boxes.push({x:495, y:27, width:4, height:3, mode:1});
        boxes.push({x:498, y:89, width:5, height:4, mode:1});
        boxes.push({x:516, y:142, width:4, height:4, mode:1});
    }
