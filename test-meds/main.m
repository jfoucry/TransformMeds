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
	    
		if (argc == 2) {
			NSString *filePath = [NSString stringWithUTF8String:argv[1]];
		}
	    else if (argc >)
	    {
	    	NSLog(@"To many argument supplied\n");
	    	return 255;
	    } 
	    else {
	    	NSLog(@"One argument expected\n");
	    	return 255;
	    } 

	    NSFileManager *fileManager = [NSFileManager defaultManager];

	    if ([fileManager fileExistsAtPath:filePath])
	    {
	    	/* code */
	    
		    NSLog(@"Start process");
			NSArray *oldMedsArray = [NSArray arrayWithContentsOfFile:filePath];
			
			NSMutableDictionary *medsDict = [[NSMutableDictionary alloc] init];
			for (NSDictionary *aDict in oldMedsArray) {
				NSString *key = [aDict objectForKey:@"cip7"];
	//			NSLog(@"key ==%@",key);
				[medsDict setObject:aDict forKey:key];
			}
			
			[medsDict writeToFile:@"/tmp/Meds-new.plist" atomically:NO];
			NSLog(@"End process");
		}
		else {
			printf("Error, %s not found\n", [filePath UTF8String]);
			return 255;
		}
	}
    return 0;
}

