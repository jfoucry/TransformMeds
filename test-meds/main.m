//
//  main.m
//  test-meds
//
//  Created by Jacques Foucry on 16/04/13.
//  Copyright (c) 2013 Jacques Foucry. All rights reserved.
//

#import <Foundation/Foundation.h>

int main(int argc, const char * argv[])
{

	@autoreleasepool {
	    
	    // insert code here...
	    NSLog(@"Start process");
		NSArray *oldMedsArray = [NSArray arrayWithContentsOfFile:@"/tmp/meds.plist"];
		
		NSMutableDictionary *medsDict = [[NSMutableDictionary alloc] init];
		for (NSDictionary *aDict in oldMedsArray) {
			NSString *key = [aDict objectForKey:@"cip7"];
//			NSLog(@"key ==%@",key);
			[medsDict setObject:aDict forKey:key];
		}
		
		[medsDict writeToFile:@"/tmp/Meds-new.plist" atomically:NO];
		NSLog(@"End process");
	}
    return 0;
}

