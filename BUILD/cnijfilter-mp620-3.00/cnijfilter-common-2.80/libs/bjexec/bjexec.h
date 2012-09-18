/*
 *  CUPS add-on module for Canon Inkjet Printer.
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

#ifndef _bjexec_
#define _bjexec_


typedef int GetDataCb (char *recv_buf, int width_bytes, void *cb_param);

int exec_filter(char* cmd_path, char* cmd_params[], int ofd, int fds[2]);
char* make_filter_param_line(char *model, int reso, ParamList *pl);
char** make_filter_param_list(char *model, int reso,
		ParamList *pl, ParamList **cmd_list);
int output_data(int out_fd, int width, int height, int bps, int num_chan,
	GetDataCb *get_data_cb, void *cb_param);

#endif	// _bjexec_

