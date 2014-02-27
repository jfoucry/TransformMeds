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
	    
	    if (argc == 0)
	    {
	    	printf("You must provide path to file to transform\n");
	    	return 255;
	    } else if (argc > 1)
	    {
	    	printf("Too much argument. You just need to provide path to file to transform\n");
	    	return 255;
	    }
	    NSString *filePath = [NSString stringWithUTF8Stringärgv[1]];

	    NSFIleManager *fileManager = [NSFIleManager defaultManager];

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
			printf("Error, %@ not found\n", filePath);
			return 255;
		}
	}
    return 0;
}

