//
//  NativeAppDelegate.h
//  Native
//
//  Copyright www.bithexagon.com 2014. All rights reserved.
//

#import <UIKit/UIKit.h>

@class NativeViewController;

@interface NativeAppDelegate : NSObject <UIApplicationDelegate> {
    UIWindow *window;
    NativeViewController *viewController;
}

@property (nonatomic, retain) IBOutlet UIWindow *window;
@property (nonatomic, retain) IBOutlet NativeViewController *viewController;

@end

