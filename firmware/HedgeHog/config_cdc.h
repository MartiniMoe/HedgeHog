/*******************************************************************************
 FileName:     	config_cdc.h
 Dependencies:
 Processor:	PIC18F46J50
 Hardware:	Porcupine HedgeHog BASIC, OLED or TESTBED
 Compiler:  	Microchip C18
 Author:        KristofVL
 ******************************************************************************/
#include "USB/usb_function_cdc.h"

#ifndef CONFIG_CDC_H
#define	CONFIG_CDC_H



/******************************************************************************/

#define cdc_start_set_time()    { config_cycle = 7;     config_mode = uart_c; }
#define cdc_start_stop_time()   { config_cycle = 7;     config_mode = uart_c; }
#define cdc_start_read()        { config_cycle = 105;   config_mode = uart_c; }
#define cdc_start_log()         { config_cycle = 55;    config_mode = uart_c; }
#define cdc_start_format()      { config_cycle = 250;   config_mode = uart_c; }
#define cdc_start_erase()       { config_cycle = 640;   config_mode = uart_c; }
#define cdc_start_init()        { config_cycle = 105;   config_mode = uart_c; }
#define cdc_start_conf_read()   { config_cycle = 55;    config_mode = uart_c; }
#define cdc_start_conf_write()  { config_cycle = 21;    config_mode = uart_c; }
#define cdc_start_reset()       { config_cycle = 17;    config_mode = uart_c; }

extern UINT16 config_cycle;
static UINT8 config_mode;

/******************************************************************************/
void config_cdc_init(void);
void up_cdc_cycle(void);
BYTE cdc_config_cmd(BYTE c);
void cdc_main_menu( rom char* name_str, rom char* ver_str);
void cdc_print_ver(rom char* name_str, rom char* ver_str);
void cdc_print_help(void);
void cdc_print_init(UINT32_VAL msg);
void cdc_print_all(BYTE x,BYTE y,BYTE z,UINT16 l,BYTE t,char* dstr,char* tstr);
void cdc_write_ok(void);
void cdc_eol(void);
void cdc_write_refat(void);
void cdc_write_log(void);
void cdc_write_conf(char* cstr);
BYTE cdc_get_conf(char *confstr, BYTE conflen);
/******************************************************************************/

#endif	// CONFIG_CDC_H
