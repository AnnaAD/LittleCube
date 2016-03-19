//
//  NativeAppDelegate.m
//  Native
//
//  Copyright www.bithexagon.com. All rights reserved.
//

#import "NativeAppDelegate.h"
#import "NativeViewController.h"

@implementation NativeAppDelegate

@synthesize window;
@synthesize viewController;


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {    
    
    // Override point for customization after app launch    
    [window addSubview:viewController.view];
    [window makeKeyAndVisible];
    
    [[UIApplication sharedApplication] setStatusBarHidden:YES];
    // printf("hello\n");
	
	return YES;
}


- (void)dealloc {
    [viewController release];
    [window release];
    [super dealloc];
}


@end
