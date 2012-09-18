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

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include <sys/types.h>
#include <sys/wait.h>


#include "paramlist.h"
#include "bjexec.h"


#define FILTER_PATH		"/usr/local/bin/"
#define FILTER_EXEC		"cif"


int exec_filter(char* cmd_path, char* cmd_params[], int ofd, int fds[2])
{
	int status = 0;
	int	child_pid = -1;

	if( pipe(fds) >= 0 )
	{
		child_pid = fork();

		if( child_pid == 0 )
		{
			close(0);
			dup2(fds[0], 0);
			close(fds[0]);
			close(fds[1]);

			if( ofd != 1 )
			{
				close(1);
				dup2(ofd, 1);
				close(ofd);
			}

			execv(cmd_path, cmd_params);
						
			fprintf(stderr, "execl() error\n");
			status = -1;
		}
		else if( child_pid != -1 )
		{
			close(fds[0]);
		}
	}
	return child_pid;
}

char* make_filter_param_line(char *model, int reso, ParamList *pl)
{
	ParamList *cmd_list = NULL;
	char *cmd_buf = NULL;
	char **cmd_param;

	cmd_param = make_filter_param_list(model, reso, pl, &cmd_list);

	if( cmd_param )
	{
		int buf_len = 0;
		int i;

		for( i = 0 ; cmd_param[i] != NULL ; i++ )
		{
			if( i == 1 )
				continue;
			buf_len += strlen(cmd_param[i]) + 2;
		}

		cmd_buf = malloc(buf_len);

		if( cmd_buf != NULL )
		{
			*cmd_buf = 0;

			for( i = 0 ; cmd_param[i] != NULL ; i++ )
			{
				if( i == 1 )
					continue;
				strcat(cmd_buf, cmd_param[i]);
				strcat(cmd_buf, " ");
			}
			cmd_buf[buf_len - 2] = 0;
		}
		free(cmd_param);
	}

	if( cmd_list != NULL )
		param_list_free(cmd_list);

	return cmd_buf;
}

char** make_filter_param_list(char *model, int reso,
		ParamList *pl, ParamList **cmd_list)
{
	char* cmd_name = NULL;
	char* cmd_path = NULL;
	ParamList *curs;
	int cmd_num;
	char **cmd_buf;
	int cmd_buf_index;
	char reso_buf[MAX_VALUE_SIZE + 1];

	// Make command path.
	cmd_name = (char*)malloc(strlen(FILTER_EXEC) + strlen(model) + 1);
	strcpy(cmd_name, FILTER_EXEC);
	strcat(cmd_name, model);

	cmd_path =  (char*)malloc(strlen(FILTER_PATH) + strlen(cmd_name));
	strcpy(cmd_path, FILTER_PATH);
	strcat(cmd_path, cmd_name);

	for( curs = pl ; curs != NULL ; curs = curs->next )
	{
		char value_buf[MAX_VALUE_SIZE + 1];

		if( strlen(curs->key) + 1 > MAX_KEY_SIZE )
			continue;
		if( curs->value_size + 1 > MAX_VALUE_SIZE )
			continue;

		memcpy(value_buf, curs->value, curs->value_size);
		value_buf[curs->value_size] = 0;

		param_list_add(cmd_list, curs->key, value_buf, curs->value_size + 1);
	}

	// Make resolution string.
	sprintf(reso_buf, "%d", reso);
	param_list_add(cmd_list, "--imageres", reso_buf, strlen(reso_buf) + 1);

	cmd_num = param_list_num(*cmd_list);
	cmd_buf = (char**)malloc((cmd_num * 2 + 3) * sizeof(char*));

	cmd_buf[0] = cmd_path;
	cmd_buf[1] = cmd_name;
	cmd_buf_index = 2;

	for( curs = *cmd_list ; curs != NULL ; curs = curs->next )
	{
		if( strcmp(curs->value, "false") )
		{
			cmd_buf[cmd_buf_index++] = curs->key;
			if( strcmp(curs->value, "true") )
			{
				cmd_buf[cmd_buf_index++] = curs->value;
			}
		}
	}
	cmd_buf[cmd_buf_index] = NULL;

	return cmd_buf;
}

int output_data(int out_fd, int width, int height, int bps, int num_chan,
	GetDataCb *get_data_cb, void *cb_param) 
{
	char pnm_header[64];
	char tmp[64];
	int write_size;
	int width_bytes;
	int lines_read;
	char* recv_buf = NULL;
	int write_bytes;
	int status;

	memset(pnm_header, 0, sizeof(pnm_header));

	if( bps == 8 && num_chan == 3 )
	{
		strcpy(pnm_header, "P6\n");
	}
	else
		return -1;

	sprintf(tmp, "%d", width);
	strcat(pnm_header, tmp);
	strcat(pnm_header, " ");
	sprintf(tmp, "%d", height);
	strcat(pnm_header, tmp);
	strcat(pnm_header, "\n");

	strcat(pnm_header, "255\n");

	write_size = strlen(pnm_header);
	status = write(out_fd, pnm_header, write_size);

	if( status != write_size )
		return -1;

	width_bytes = (num_chan * bps * width + 7) >> 3;

	if( (recv_buf = (char*)malloc(width_bytes)) == NULL )
		return -1;

	status = 0;
	for( lines_read = 0 ; lines_read < height ; lines_read++ )
	{
		status = get_data_cb(recv_buf, width_bytes, cb_param);

		if(status == 2)
		{
			status = 0;
			break;
		}
		else if(status != 0)
			break;

		write_bytes = write(out_fd, recv_buf, width_bytes);
		if( write_bytes != width_bytes )
		{
			status = -1;
			break;
		}
	}

	free(recv_buf);

	return status;
}

