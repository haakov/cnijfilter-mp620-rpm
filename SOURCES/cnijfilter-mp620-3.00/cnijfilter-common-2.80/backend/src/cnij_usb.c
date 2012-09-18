/*
 *  Canon Inkjet Printer Driver for Linux
 *  Copyright CANON INC. 2001-2007
 *  All Rights Reserved.
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

//
//  '2004.05.25
//  Using the original "usb.c" code of the CUPS 1.1.14 to create a new
//  backend for writing the printing data into a named pipe.
//

/*
 *
 *   USB port backend for the Common UNIX Printing System (CUPS).
 *
 *   Copyright 1997-2002 by Easy Software Products, all rights reserved.
 *
 *   These coded instructions, statements, and computer programs are the
 *   property of Easy Software Products and are protected by Federal
 *   copyright law.  Distribution and use rights are outlined in the file
 *   "LICENSE" which should have been included with this file.  If this
 *   file is missing or damaged please contact Easy Software Products
 *   at:
 *
 *       Attn: CUPS Licensing Information
 *       Easy Software Products
 *       44141 Airport View Drive, Suite 204
 *       Hollywood, Maryland 20636-3111 USA
 *
 *       Voice: (301) 373-9603
 *       EMail: cups-info@cups.org
 *         WWW: http://www.cups.org
 *
 * Contents:
 *
 *   main()         - Send a file to the specified USB port.
 *   list_devices() - List all USB devices.
 */

#include <cups/cups.h>
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>

#if defined(WIN32) || defined(__EMX__)
#  include <io.h>
#else
#  include <unistd.h>
#  include <fcntl.h>
#  include <termios.h>
#endif /* WIN32 || __EMX__ */

#include "cnij_common_function.h"


/*
 * Local functions...
 */

void	list_devices(void);

/*
 * 'main()' - Send a file to the specified USB port.
 *
 * Usage:
 *
 *    printer-uri job-id user title copies options [file]
 */

int			/* O - Exit status */
main(int  argc,		/* I - Number of command-line arguments (6 or 7) */
     char *argv[])	/* I - Command-line arguments */
{
	char	method[255],			/* Method in URI 				   	*/
			hostname[1024],			/* Hostname 						*/
			username[255],			/* Username info (not used) 		*/
			resource[1024],			/* Resource info (device and options) */
			*options;				/* Pointer to options 				*/
	int		port;					/* Port number (not used) 			*/
	FILE	*fp;					/* Print file 						*/
	int		copies;					/* Number of copies to print 		*/
	int		fd;						/* USB device 						*/

 /*
  * Make sure status messages are not buffered...
  */

	setbuf(stderr, NULL);

	/*
	* Check command-line...
	*/

	if (argc == 1)
	{
		list_devices();
		return (0);
	}
	else if (argc < 6 || argc > 7)
	{
		fputs("Usage: USB job-id user title copies options [file]\n", stderr);
		return (1);
	}

	/*
	* If we have 7 arguments, print the file named on the command-line.
	* Otherwise, send stdin instead...
	*/

	if (argc == 6)
	{
		fp     = stdin;
		copies = 1;
	}
	else
	{
		/*
		* Try to open the print file...
		*/

		if ((fp = fopen(argv[6], "rb")) == NULL)
		{
			perror("ERROR: unable to open print file");
			return (1);
		}

		copies = atoi(argv[4]);
	}

	/*
	* Extract the device name and options from the URI...
	*/
/*
 *	httpSeparate(argv[0], method, username, hostname, &port, resource);
 *  This function is deprecated under CUPS 1.2, so we(Canon) do not
 *  use it, instead, parse the argv[0] by ourselves as following.
 */
	if ((strncmp(argv[0], "cnij_usb:/dev", 13) == 0))
	{
		memset(resource, 0, 1024);
		strncpy(resource, argv[0] + 9, 1023);
	}
	else
	{
		perror("ERROR: Illegal backend");
		return (1);
	}

	/*
	* See if there are any options...
	*/

	if ((options = strchr(resource, '?')) != NULL)
	{
		/*
		* Yup, terminate the device name string and move to the first
		* character of the options...
		*/

		*options++ = '\0';
	}

	/*
	* Open the USB port device...
	*/


	do
	{
		if ((fd = open(resource, O_RDWR | O_EXCL)) == -1)
		{
			if (errno == EBUSY)
			{
				fputs("INFO: USB port busy; will retry in 30 seconds...\n", stderr);
				sleep(30);
			}
			else
			{
				perror("ERROR: Unable to open USB port device file");
				return (1);
			}
		}
	}
	while (fd < 0);

	_canon_bj( argc, fp, fd, copies, argv[5] ) ;

	/*
	* Close the socket connection and input file and return...
	*/

    close( fd ) ;                               /* device fd close          */
	if	( fp != stdin )
	fclose( fp ) ;

	return( 0 ) ;
}

/*
 * 'list_devices()' - List all USB devices.
 */

void
list_devices(void)
{
#ifdef __linux
  int	i;			/* Looping var */
  int	fd;			/* File descriptor */
  char	device[255];		/* Device filename */
  FILE	*probe;			/* /proc/bus/usb/devices file */
  char	line[1024],		/* Line from file */
	*delim,			/* Delimiter in file */
	make[IPP_MAX_NAME],	/* Make from file */
	model[IPP_MAX_NAME];	/* Model from file */


 /*
  * First try opening one of the USB devices to load the driver
  * module as needed...
  */

  if ((fd = open("/dev/usb/lp0", O_WRONLY)) >= 0)
    close(fd); /* 2.3.x and 2.4.x */
  else if ((fd = open("/dev/usb/usblp0", O_WRONLY)) >= 0)
    close(fd); /* Mandrake 7.x */
  else if ((fd = open("/dev/usblp0", O_WRONLY)) >= 0)
    close(fd); /* 2.2.x */

 /*
  * Then look at the device list for the USB bus...
  */

  if ((probe = fopen("/proc/bus/usb/devices", "r")) != NULL)
  {
   /*
    * Scan the device list...
    */

    i = 0;

    memset(make, 0, sizeof(make));
    memset(model, 0, sizeof(model));

    while (fgets(line, sizeof(line), probe) != NULL)
    {
     /*
      * Strip trailing newline.
      */

      if ((delim = strrchr(line, '\n')) != NULL)
	*delim = '\0';

     /*
      * See if it is a printer device ("P: ...")
      */

      if (strncmp(line, "S:", 2) == 0)
      {
       /*
        * String attribute...
	*/

        if (strncmp(line, "S:  Manufacturer=", 17) == 0)
	{
	  strncpy(make, line + 17, sizeof(make) - 1);
	  if (strcmp(make, "Canon") == 0)
	    strcpy(make, "Canon");
	}
        else if (strncmp(line, "S:  Product=", 12) == 0)
	  strncpy(model, line + 12, sizeof(model) - 1);
      }
      else if (strncmp(line, "I:", 2) == 0 &&
               (strstr(line, "Driver=printer") != NULL ||
	        strstr(line, "Driver=usblp") != NULL) &&
	       make[0] && model[0])
      {
       /*
        * We were processing a printer device; send the info out...
	*/

        sprintf(device, "/dev/usb/lp%d", i);
	if (access(device, 0))
	{
	  sprintf(device, "/dev/usb/usblp%d", i);

	  if (access(device, 0))
	    sprintf(device, "/dev/usblp%d", i);
	}

	printf("direct cnij_usb:%s \"%s %s\" \"USB Printer #%d with status readback for Canon IJ\"\n",
	       device, make, model, i + 1);

	i ++;

	memset(make, 0, sizeof(make));
	memset(model, 0, sizeof(model));
      }
    }

    fclose(probe);

   /*
    * Write empty device listings for unused USB devices...
    */

    for (; i < 16; i ++)
    {
      sprintf(device, "/dev/usb/lp%d", i);

      if (access(device, 0))
      {
	sprintf(device, "/dev/usb/usblp%d", i);

	if (access(device, 0))
	{
	  sprintf(device, "/dev/usblp%d", i);

	  if (access(device, 0))
	    continue;
	}
      }

      printf("direct cnij_usb:%s \"Unknown\" \"USB Printer #%d with status readback for Canon IJ\"\n", device, i + 1);
    }
  }
  else
  {
   /*
    * Just check manually for USB devices...
    */

    for (i = 0; i < 16; i ++)
    {
      sprintf(device, "/dev/usb/lp%d", i);

      if (access(device, 0))
      {
	sprintf(device, "/dev/usb/usblp%d", i);

	if (access(device, 0))
	{
	  sprintf(device, "/dev/usblp%d", i);

	  if (access(device, 0))
	    continue;
	}
      }

      printf("direct cnij_usb:%s \"Unknown\" \"USB Printer #%d with status readback for Canon IJ\"\n", device, i + 1);
    }
  }
#elif defined(__sgi)
#elif defined(__sun)
#elif defined(__hpux)
#elif defined(__osf)
#elif defined(__FreeBSD__)
  int   i;                      /* Looping var */
  char  device[255];            /* Device filename */


  for (i = 0; i < 3; i ++)
  {
    sprintf(device, "/dev/unlpt%d", i);
    if (!access(device, 0))
      printf("direct cnij_usb:%s \"Unknown\" \"USB Printer #%d with status readback for Canon IJ\"\n", device, i + 1);
  }
#elif defined(__NetBSD__) || defined(__OpenBSD__)
  int   i;                      /* Looping var */
  char  device[255];            /* Device filename */


  for (i = 0; i < 3; i ++)
  {
    sprintf(device, "/dev/ulpt%d", i);
    if (!access(device, 0))
      printf("direct cnij_usb:%s \"Unknown\" \"USB Printer #%d with status readback for Canon IJ\"\n", device, i + 1);
  }
#endif
}

