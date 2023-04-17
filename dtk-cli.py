#####################################################################
### dtk-cli.py -- DEVELOPER TOOLKIT COMMAND LINE INTERFACE OBJECT ###
#####################################################################
__author__="Eamon Smith (github.com/34m0n-dev)"
__version__='1.0'
__created__='4/3/2023, Monday'

##############
### SYSTEM ###
##############
import sys
import os
import pathlib
from pathlib import Path
import shutil
import argparse
import string
import operator
import datetime
from datetime import datetime

#########################
### DATA MANIPULATION ###
#########################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import csv
import str

############
### MISC ###
############
import webbrowser
import hashlib
from hashlib import sha256
import math
from math import floor

#######################
### main() FUNCTION ###
#######################
def main(author=__author__, version=__version__, created=__created__):

    ################
    ### ARGPARSE ###
    ################
    parser=argparse.ArgumentParser(description=argparse_CLI_description, formatter_class=argparse_formatter_class)
    parser.add_argument('-f','--file-path',dest='filepath',metavar='file path',help='Direct path input to access desired dev-toolkit function.', required=True, default=os.getcwd())
    parser.add_argument('-h','--home-path',dest='homepath',metavar='home path',help='Sets the home path for the command line interface. Default is the directory containing the dtk-cli.py file.', required=True, default=os.getcwd())
    parser.add_argument('-w','--width-limit', dest='width_limit',metavar='number',help='Sets the character limit per line in the command line interface. This must be an integer! Default is 69.',required=True,default=69)
    parser.add_argument('-lc','--height-limit', dest='height_limit',metavar='number',help='Sets the maximum number of lines that can be taken up by the contents of a file being previewed. This must be an integer! Default is 24.',required=True,default=69)
    parser.add_argument('-nc','--navigation-cache-limit',dest='navigation_cache_limit',metavar='number',help='Specifies the number of elements that will be kept in the session cache for usage by the back/forward button commands (similar to a web browser). This input must be an integer.',required=True,default=10)
    parser.add_argument('-MO','--manual-override-pwd',dest='manual_override_pwd',help='Dev argument to access more functionality. This method means nothing without inputting the correct password, which is cross-referenced with a pre-generated hash output.', required=False, default=None)
    args=parser.parse_args()
    jump_to_path=args.filepath
    manual_override_pwd=args.manual_override_pwd
    width_limit=args.width
    height_limit=args.height_limit
    nav_cache_limit=args.navigation_cache_limit

    #####################################################
    ## DEVELOPER_TOOLKIT_COMMAND_LINE_INTERFACE CLASS ###
    #####################################################
    class DEVELOPER_TOOLKIT_COMMAND_LINE_INTERFACE:

        #################################
        ### INIT EXCLUSIVE OPERATIONS ###
        #################################
        def __os_syntax_profiling(self):
            platforms='linux1':'linux','linux2':'linux','darwin':'os_x','win32':'windows'}
            slashes={'linux':'/','windows':r'\\','os_x':'/'}
            sys_os=sys.platform if sys.platform not in platforms else platforms[sys.platform]
            sys_slashes=slashes['linux'] if sys_os not in slashes else slashes[sys_os] # assume linux syntax for slashes used in path strs
            self.sys_os=sys_os
            self.sys_slashes=sys_slashes
        def __establish_paths(self, src_dir_path):
            src_dir_path=os.getcwd() if src_dir_path is None else src_dir_path
            sys.path.append(src_dir_path)
            self.src_dir_path=src_dir_path
            self.bookmarks_path=self.src_dir_path + self.sys_slashes + 'bookmarks.json' + self.sys_slashes
            self.usage_data_path=self.src_dir_path + self.sys_slashes + 'usage_data.json' + self.sys_slashes
            self.default_settings_path=self.src_dir_path + self.sys_slashes + 'default_settings.json' + self.sys_slashes
            self.current_settings_path=self.src_dir_path + self.sys_slashes + 'current_user_settings.json' + self.sys_slashes
            self.cmd_metadata_path=src_dir_path + sys_slashes + 'commands.json' + sys_slashes
            self.desktop_path = (os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) # may encounter difficulties if the DTK-CLI folder is not located somewhere on desktop, thus doing so is recommended for ease of use. Otherwise, you will need to pass something else though here.
        def __load_bookmarks(self):
            self.bookmarks_path=self.src_dir_path + self.sys_slashes + 'bookmarks.json' + self.sys_slashes
            if os.path.isfile(self.bookmarks_path):
                with open(self.bookmarks_path, "r") as iter_json_to_load:
                    bookmarks=json.load(iter_json_to_load)
            else:
                bookmarks={self.__fetch_desktop_path():{'name':'Desktop','bookmark_usage_count':0},
                             src_dir_path:{'name':'Toolkit Home','bookmark_usage_count':0}}
                with with open(self.bookmarks_path, "w") as outfile:
                    json.dump(bookmarks, outfile)
            self.bookmarks=bookmarks
        def __load_usage_data(self):
            self.usage_data_path=self.src_dir_path + self.sys_slashes + 'usage_data.json' + self.sys_slashes
            if os.path.isfile(self.usage_data_path):
                with open(self.usage_data_path, "r") as iter_json_to_load:
                    usage_data=json.load(iter_json_to_load)
            else:
                usage_data={self.__fetch_desktop_path():0,
                             src_dir_path():0}
                with with open(self.usage_data_path, "w") as outfile:
                    json.dump(usage_data, outfile)
            self.usage_data=usage_data
        def __load_default_settings(self):
            self.default_settings_path=self.src_dir_path + self.sys_slashes + 'default_settings.json' + self.sys_slashes
            if os.path.isfile(self.default_settings_path):
                with open(self.default_settings_path, "r") as iter_json_to_load:
                    default_settings=json.load(iter_json_to_load)
            else:
                default_settings={
                                    'HomePathString':self.src_dir_path,
                                    'DesktopPathString':self.desktop_path,
                                    'NavigationCacheSizeLimit':self.nav_cache_limit,
                                    'LineCharWidthLimit':self.width_limit,
                                    'PreviewLineHeightLimit':self.height_limit,
                                    'DividerLarge':'X',
                                    'DividerLarge_proportion':1,
                                    'DividerMedium':'~',
                                    'DividerMedium_proportion':2.5,
                                    'DividerSmall':'-',
                                    'DividerSmall_proportion':3.3,
                                    'ManualOverridePwd':self.manual_override_pwd,
                                    'StatusBarDateTimeFormat':"%H:%M:%S",
                                    'StatusBarPosition':'bottom' # 'top' or 'bottom'
                                    'PrintInterfaceMetadata':True
                                    'RESET_TO_DEFAULT':False
                                   }
                with with open(self.default_settings_path, "w") as outfile:
                    json.dump(default_settings, outfile)
            self.default_settings=default_settings
        def __load_current_settings(self):
            self.current_settings_path=self.src_dir_path + self.sys_slashes + 'current_user_settings.json' + self.sys_slashes
            if os.path.isfile(self.current_settings_path):
                with open(self.current_settings_path, "r") as iter_json_to_load:
                    current_settings=json.load(iter_json_to_load)
            else:
                current_settings=__load_default_settings(self)
                with with open(self.current_settings_path, "w") as outfile:
                    json.dump(current_settings, outfile)
            self.current_settings=current_settings
        def __load_cmd_metadata(self, src_dir_path, sys_slashes):
            self.cmd_metadata_path=src_dir_path + sys_slashes + 'commands.json' + sys_slashes
            if os.path.isfile(self.cmd_metadata_path):
                with open(self.cmd_metadata_path, "r") as iter_json_to_load:
                    commands_metadata=json.load(iter_json_to_load)
            else:
                command_parameters={
                                    'Setting':{'CLI_syntax':'--s',
                                               'description':'This parameter is used to specify the parameter whose value we want to change when we are adjusting CLI settings.'},
                                    'Value':{'CLI_syntax':'--v',
                                             'description':'This parameter is used to specify any value used in the command.'},
                                    'Path':{'CLI_syntax':'--p',
                                            'description':'This parameter is used to specify the strings for any paths used in the command.'},
                                    'Name':{'CLI_syntax':'--n',
                                            'description':'This parameter is used to specify the name of any object during command execution.'},
                                    'Bookmark':{'CLI_syntax':'--b',
                                                'description':'This parameter can either be the name of a bookmark or the string of the path for the bookmark. The CLI will automatically process both.'},
                                    'execManualStr':{ 'CLI_syntax':'--exs',
                                                     'description':'This parameter can specify either the path of a .txt file which contains the string of code which will be run via exec(). The parameter can also just be the string to be passed through exec() as well--the CLI will attempt to distinguish this by checking if the string is a valid path.'}
                                   }
                global_commands={
                                 'ExitCLI':{'description':'Exit the toolkit command line interface.',
                                            'CLI_syntax':'X',
                                            'allowed_variations':['ExitCLI','x','X','exit()','exit','EXIT','esc','ESC','/exit','/EXIT','/X','/x','x()','X()'], # references allowed variations for input arguments to trigger this command
                                            'details':None},
                                 'ReturnToHomePage':{'description':'Return to the home view on the CLI',
                                                     'CLI_syntax':'H',
                                                     'allowed_variations':['ReturnToHomePage','h','H','Home','HOME','/home','home()','/h','/H'],
                                                     'details':None},
                                 'ToggleHelpMenuDisplay':{'description':'Opens/closes up the help menu on the CLI.',
                                                       'CLI_syntax':'?',
                                                       'allowed_variations':['ToggleHelpMenuDisplay','?', 'Help','HELP','/help','/?','/h','/H','/HELP','help()'],
                                                       'details':None},
                                 'ToggleSettingsDisplay':{'description':'Opens/closes up the settings menu.',
                                                          'CLI_syntax':'S',
                                                          'allowed_variations':['Settings','S','s','/settings','SETTINGS','/S','/s', 'settings()'],
                                                          'details':None},
                                 'ToggleSettingValue':{'description': 'Allows for any of the values in the settings to be adjusted. These commands can also be triggered outside of the settings menu itself.',
                                                       'CLI_syntax':'S --s [PARAMETER] --v [VALUE]',
                                                       'allowed_variations':['SETTINGS --p [PARAMETER] --v [VALUE]', 'S --p [PARAMETER] --v [VALUE]', 'settings([PARAMETER], [VALUE])', '/settings [PARAMETER] [VALUE]'],
                                                       'details':None},
                                 'OpenBookmarksBar':{'description':'Opens the bookmarks bar window, where either default or previous bookmarks are loaded for access.',
                                                     'CLI_syntax':'BK',
                                                     'allowed_variations':['OpenBookmarksBar','/OpenBookmarksBar','OpenBookmarksBar()','BOOKMARKS','BK','Bookmarks','bk','bookmarks()','','','',''],
                                                     'details':None},
                                 'OpenBookmark':{'description':'Opens the bookmark specified by the name of the bookmark or the path of the bookmark.',
                                                 'CLI_syntax':'OB --',
                                                 'allowed_variations':[],
                                                 'details':None}
                }
                path_commands={
                                 'TeleportToSpecifiedPath':{'description':'Shifts the CLI window to a view at the path str or the name of the file. This ideally is the full path str.',
                                                           'CLI_syntax':'BK',
                                                           'allowed_variations':['TeleportToSpecifiedPath --id [ID]','/TeleportToSpecifiedPath --id [ID]', 'TP --id [ID]','tp --id [ID]', 'chdir --id [ID]', 'cd --id [ID]', 'cd --id [ID]', '/tp PATH', '/tp --id [ID]','/TP --id [ID]','/TP --id [ID]','teleport(--id [ID])','tp(--id [ID])']},
                                                           'details':None},
                                 'NavigateForward':{'description':'The same as a forward button on a web browser.',
                                                    'CLI_syntax':'>',
                                                    'allowed_variations':['Foward','f','F','forward','FORWARD', '>','forward()','/forward','/f'],
                                                    'details':None},
                                 'NavigateBack':{'description':'The same as a back button on a web browser.',
                                                 'CLI_syntax':'<',
                                                 'allowed_variations':['Back','B', 'back','b', ' BACK', '<','back()','/back','/b'],
                                                 'details':None},
                                 'ParentDirectory':{'description':'Moves the interface window path to the to the parent of the current directory.',
                                                    'CLI_syntax':'PD',
                                                    'allowed_variations':['ParentDirectory','/ParentDirectory','P','p','parent','PARENT','..','<<','parent()','/p','/parent','/P','parent()'],
                                                    'details':None},
                                 'PrintContents':{'description':'Prints the contents of the file within the command line interface. This method removes all formatting with regard to width specifications to maintain the original layout of the file.',
                                                  'CLI_syntax':'PFC',
                                                  'allowed_variations':['PrintFileContents','/PrintFileContents', 'PF-C','PrintFileContents()','Contents()','pf-c','/PF-C','/pf-c'],
                                                  'details':None},
                                 'PrintPreview':{'description':'Prints a preview of the contents of a file, which has a max line count of the -lc (--preview-height) parameter. Depending on the file, this summary may be more detailed than just the first height_limit lines of a file.',
                                                 'CLI_syntax':'PFP',
                                                 'allowed_variations':['PrintFilePreview','pf-p','PREVIEW','PF-P','Preview()','PrintFilePreview()','/pf-p','/PF-P','/preview','/PREVIEW','/PrintFilePreview'],
                                                 'details':None},
                                 'SaveCurrentPathAsBookmark':{'description':'Saves the directory path associated with the current interface window as a bookmark. Running this command will prompt a second input for the bookmark name unless it is also specified in the first call.',
                                                              'CLI_syntax':'SBK --n [NAME]',
                                                              'allowed_variations':['SaveCurrentPathAsBookmark --n [NAME]','/SaveCurrentPathAsBookmark --n [NAME]','SaveCurrentPathAsBookmark([NAME])','SBK --n [NAME]','/SBK --n [NAME]','SBK([NAME])','sbk --n [NAME]','/sbk --n [NAME]','sb([NAME])'],
                                                              'details':None},
                }
                EXEC_WARNING_TEXT='Only available with manual override. WARNING: THIS FUNCTION IS VERY DANGEROUS. MAKE SURE YOU KNOW EXACTLY WHAT YOU ARE PASSING THROUGH EXEC().'
                manual_commands={'execStringInput':{'description':(EXEC_WARNING_TEXT + '\nThe interface will prompt another input upon calling this command, and the str next inputted by the user will be passed through the exec() function (native to python). The methods of calling the command involving [TXT_PATH] refer to the path of a .txt file containing the str which can be passed through exec() (this removes limitations for being limited to a single line of code).'),
                                                      'CLI_syntax':'execStringInput',
                                                      'allowed_variations':['execStringInput','/execStringInput','execStringInput()', 'execStringInput --txt [TXT_PATH]','/execStringInput --txt [TXT_PATH]','execStringInput([TXT_PATH])'],
                                                      'details':None}
                }
                commands_metadata={
                                   'command_parameters':command_parameters,
                                   'global_commands':global_commands,
                                   'path_commands':directory_commands,
                                   'manual_commands':manual_override_on_only_commands
                                   }
                with open(self.cmd_metadata_path, "w") as outfile:
                    json.dump(commands_metadata, outfile)
            self.cmd_metadata=commands_metadata
        def __check_manual_override_credentials(self, manual_override_pwd):
            if manual_override_pwd==None:
                self.manual_override_mode=False
            else:
                manual_override_pwd_hash=hashlib.sha256(manual_override_pwd.encode()).hexdigest()
                reference_hash="6f943458264a2e5b9136549a82127f03c161bd91afbe0f93e807e35f9cb1e7ca"
                correct_pwd_entered=True if (manual_override_pwd==reference_hash) else False
                if not correct_pwd_entered:
                    print("ERROR: THE CORRECT STRING FOR THE INPUT ARGUMENT manual_override_pwd WAS NOT PASSED. THE PROGRAM WILL STILL LAUNCH, BUT FUNCTIONALITIES PERTAINING TO 'MANUAL OVERRIDE MODE' WILL BE INACCESSIBLE.")
                self.manual_override_mode=correct_pwd_entered
        def __proportioned_divider_strs(self):
            divider_proportions={'DividerLarge':self.current_settings['DividerLarge_proportion'],
                                 'DividerMedium':self.current_settings['DividerMedium_proportion'],
                                 'DividerSmall':self.current_settings['DividerSmall_proportion']}
            proportioned_large=(self.current_settings['DividerLarge'] * floor((self.current_settings['LineWidthLimit'] / divider_proportions['DividerLarge'])))
            proportioned_medium=(self.current_settings['DividerMedium'] * floor((self.current_settings['LineWidthLimit'] / divider_proportions['DividerMedium'])))
            proportioned_small=(self.current_settings['DividerSmall'] * floor((self.current_settings['LineWidthLimit'] / divider_proportions['DividerSmall'])))
            proportioned_output_dividers={'DividerLarge':{'unit':self.current_user_settings['DividerLarge'],
                                                            'proportioned':proportioned_large},
                                            'DividerMedium':{'unit':self.current_user_settings['DividerMedium'],
                                                             'proportioned':proportioned_medium},
                                            'DividerSmall':{'unit':self.current_user_settings['DividerSmall'],
                                                            'proportioned':proportioned_small}}
            self.dividers=proportioned_output_dividers
                    ### INIT ###

        ######################
        ### CLI OPERATIONS ###
        ######################
        def __get_all_valid_commands_for_current_windows(self):
            output_valid_commands_dict=self.cmd_metadata['manual_commands'] if self.manual_override_mode else {}
            for cmdi in self.cmd_metadata['global_commands']:
                output_valid_commands_dict[cmdi]=self.cmd_metadata['global_commands'][cmdi]
            for cmdi in self.cmd_metadata['path_commands']:
                if cmdi in ['TeleportToSpecifiedPath', 'NavigateForward', 'NavigateBack','ParentDirectory','SaveCurrentPathAsBookmark']:
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_commands'][cmdi]
                elif cmdi=='PrintPreview' and (self.CLI_mode=='PrintContents'):
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_commands'][cmdi]
                elif cmdi=='PrintContents' and self.CLI_mode=='PrintPreview':
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_commands'][cmdi]
            self.CLI_viable_cmds=output_valid_commands_dict
        def __update_txt_session_log(self, str_block_to_append_to_agg):
            self.session_log['saved_str_blocks'].append(str_block_to_append_to_aggregate).append('\n')
        def __update_usage_data(self, path_accessed):
            if path_accessed in [udk for udk in self.usage_data]:
                self.usage_data[path_accessed]+=1
            else:
                self.usage_data[path_accessed]=1
            for bookmarks_iter in self.bookmarks:
                self.bookmarks[bookmarks_iter]['bookmark_usage_count']=self.usage_data[bookmarks_iter]
        def __trim_navigate_forwards_or_backwards_path_history_lists(self):
            cache_size_limit=self.current_settings['NavigationCacheSizeLimit']
            if len(self.back_button_paths) > cache_size_limit:
                while len(self.back_button_paths) > cache_size_limit:
                    self.back_button_paths=self.back_button_paths[:-1]
            if len(self.forward_button_paths) > cache_size_limit:
                while len(self.forward_button_paths) > cache_size_limit:
                    self.forward_button_paths=self.forward_button_paths[:-1]
        def __open_url_on_client_browser(url_str, new=0, autoraise=True, **kwargs):
            webbrowser.open(url_str, new=new, autoraise=True, **kwargs)
        def __enumerated_key_dict(self,dict_to_enumerate):
            final_dict={}
            old_keys=[key for key in dict_to_enumerate]
            enumerated_keys=[enum_keys for enum_keys,key_name_values in enumerate(old_keys)]
            for name_key, enum_key in zip(old_keys, enumerated_keys):
                final_dict_component_dict={'name':name_key}
                name_key_values=dict_to_enumerate[name_key]
                if isinstance(name_key_values, dict):
                    sub_dict_keys=[subdict_k for subdict_k in name_key_values]
                    for sdk in sub_dict_keys:
                        final_dict_component_dict[sdk]=name_key_values[sdk]
                else:
                    final_dict_component_dict['value']=name_key_values
                final_dict[str(enum_key)]=final_dict_component_dict
            return final_dict
        def __width_limit_fmt(self,print_str):
            fmt_str_output, str_iter, new_line_chars='', print_str, ['\n',r'\n']
            no_hyphen_chars_list=[' ', '', '.', ',','!','?','<','>',';',':',"'",'"','\n',r'\n','[',']','{','}','+','=','-','_',')','(','*','^','&','%','$','#','@','1','2','3','4','5','6','7','8','9','0','``'] # if either of the last char of the current line or the first char of the next line is in this list, then a hyphen will not be added between them.
            punctuation_list=['.', ',','!','?','<','>',';',':',"'",'"',')','(','[',']','{','}','%']
            while len(str_iter) > len(''):
                current_line, next_char=str_iter[0:(width_limit-1)], str_iter[width_limit]
                str_iter=str_iter[self.width_limit:]
                if current_line[-1] not in no_hyphen_chars_list and next_char not in no_hyphen_chars_list:
                    current_line+='-'
                elif next_char in punctuation_list:
                    current_line+=next_char
                    str_iter=str_iter[1:]
                fmt_str_output+=(current_line + '\n')
            return fmt_str_output
        def __user_input_cmd_compiler(self, str_to_format):
            original_str = str_to_format
            self.__get_all_valid_commands_for_current_windows()
            valid_command_name_list=[cmdi for cmdi in self.CLI_viable_cmds]
            valid_command_syntax_list=[stx['CLI_syntax'].lower() for stx in valid_command_name_list]
            first_double_dashes_encountered=False
            cmd_input_contains_params=True if ('--' in str_to_format) else False
            cmd_name=''
            cmd_is_valid_check = True
            cmd_params_are_valid_check = True
            print_error_message=False
            if cmd_input_contains_params: # case for param parsing
                # identify core command
                cmd_str=''
                cmd_name=''
                cmd_is_valid_check = True
                while str_to_format[0:1] !- '--':
                    cmd_str+=str_to_format[0]
                    str_to_format = str_to_format[1:]
                # check to make sure specified command is valid
                if cmd_str == '':
                    cmd_is_valid_check=False
                else:
                    for cmdni in self.CLI_viable_cmds:
                        if self.CLI_viable_cmds[cmdni]['CLI_syntax'].replace(' ', '') == cmd_str.replace(' ',''):
                            cmd_name = cmdni
                    cmd_is_valid_check = True if (cmd_name in [cmdn for cmdn in self.CLI_viable_cmds]) else False
                str_to_format = str_to_format.replace((cmd_str + ' '),'').replace(cmd_str,'')
                # fill param dict
                parameter_dict={}
                for parami in self.cmd_metadata['command_parameters']:
                    if parami['CLI_syntax'] in str_to_format:
                        temp_param_subdict = self.cmd_metadata['command_parameters'][parami]
                        temp_param_subdict['input_arg'] = ''
                        parameter_dict[parami]=temp_param_subdict
                # check to make sure params are allowed with the core command
                cmd_params_are_valid_check = True
                for paramni in parameter_dict:
                    if param_dict[paramni]['CLI_syntax'] not in self.CLI_viable_cmds[cmd_name]['CLI_syntax']:
                        cmd_params_are_valid_check = False
                print_error_message=False if (cmd_is_valid_check and cmd_params_are_valid_check) else True
                # identify param values
                split_inputs_list = str_to_format.split(' ')
                current_element_is_param_syntax=True
                current_param_syntax = ''
                current_param_value = ''
                whlle len(split_inputs_list) > len([]):
                    if current_element_is_param_syntax:
                        current_param_syntax = split_inputs_list[0]
                        current_element_is_param_syntax=False
                    else:
                        current_param_value = split_inputs_list[0]
                        for paramni in parameter_dict:
                            if parameter_dict[paramni]['CLI_syntax'] == current_param_syntax:
                                parameter_dict[paramni]['input_arg']=current_param_value
                        current_element_is_param_syntax=True
                        current_param_syntax = ''
                        current_param_value = ''
                    split_inputs_list = split_inputs_list[1:]
            else: # case for just cmd identification with no params
                str_to_format=str_to_format.replace(' ','').replace('\n','').lower()
                print_error_message=False if str_to_format in valid_command_syntax_list else False
                cmd_name=''
                parameter_dict=''
                if not print_error_message:
                    for cmdni in valid_command_name_list:
                        if self.CLI_viable_cmds[cmdni]['CLI_syntax'] == str_to_format:
                            cmd_name=cmdni
                            cmd_str = self.CLI_viable_cmds[cmdni]['CLI_syntax']
            if print_error_message:
                cmd_not_accepted_error_message="""
                Error! Input command not accepted. Please try again.
                """
                print(cmd_not_accepted_error_message)
                self.__update_txt_session_log(cmd_not_accepted_error_message)
            else:
                output_cmd_dict={'original_str':original_str,
                                 'cmd_name':cmd_name,
                                 'cmd_str':cmd_str,
                                 'parameters':parameter_dict}
                return output_dict

        ########################
        ### CLI TEXT OUTPUTS ###
        ########################
        def status_bar_display(self):
            width_limit_bar=(self.dividers['DividerLarge']['proportioned'])
            output_text_str="""\n{}\n         {} \n COMMANDS:\n | HOME--> H | HELP--> ? | SETTINGS--> S |{} EXIT--> X |\n | OPEN--> O [ID] | < NAVIGATE > | BOOKMARKS--> B (--n [NAME] OR --s [PATH]) |\n{}\n{}\n""".format(width_limit_bar,datetime.now.strftime(self.current_settings['StatusBarDateTimeFormat']),(' EXEC--> E |' if self.manual_override_mode else '') os.getcwd(), width_limit_bar)
            return self.__width_limit_fmt(print_str=output_text_str)
        def ReturnToHomePage_display(self):
            output_text_str="""
            {} \nDEVELOPER TOOLKIT COMMAND LINE INTERFACE VER. {}\n  {}\n   CREATED BY {} ON {} \n  {}\n{}
            """.format(self.dividers['DividerLarge']['proportioned'],
                       self.dividers['DividerMedium']['proportioned'],
                       self.about['Version'],
                       self.about['Author'],
                       self.about['Created'],
                       self.dividers['DividerMedium']['proportioned'],
                       self.dividers['DividerLarge']['proportioned'])
            return self.__width_limit_fmt(print_str=output_text_str)
        def HelpMenu_display(self):
            top_help_str_to_display="""
            {} DEVELOPER TOOLKIT COMMAND LINE INTERFACE
                   {} HELP SCREEN (PRESS ANY KEY TO EXIT)
            """.format((self.current_settings['DividerLarge'] * floor((self.current_settings['LineWidthLimit'] / 3))), (self.current_settings['DividerMedium'] * floor((self.current_settings['LineWidthLimit'] / 5))))
            global_commands_help_text='GLOBAL COMMANDS:\n---------------\n'
            global_commands, path_commands=self.cmd_metadata['global_commands'], self.cmd_metadata['path_commands']
            global_commands_names, path_commands_names=[cmdn for cmdn in global_commands], [cmdn for cmdn in [path_commands]
            if self.manual_override_mode:
                manual_commands=self.cmd_metadata['manual_commands']
                manual_commands_names=[cmdn for cmdn in manual_commands]
            else:
                manual_commands={}
                manual_commands_names=[]
            total_commands_names=global_commands_names + path_commands_names + manual_commands_names
            for gcmd in total_commands_names:
                text_temp='[{}]: {}\n--> Called by using any of: '.format(gcmd, global_commands[gcmd]['description'])
                possible_calls_list,possible_calls_str=global_commands[gcmd]['allowed_variations'],''
                for pcalls in possible_calls_list:
                    possible_calls_str+=pcalls
                text_temp+=possible_calls_str
                global_commands_help_text+=text_temp
            output_text_str=top_help_str_to_display + global_commands_help_text
            return self.__width_limit_fmt(print_str=output_text_str)
        def SettingsMenu_display(self):
            top_display="\n{} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} SETTINGS\n{}(INPUT TO EXIT BACK TO HOME--> S)".format((self.current_settings['DividerLarge'] * floor((self.current_settings['LineWidthLimit'] / 3))), (self.current_settings['DividerMedium'] * floor((self.current_settings['LineWidthLimit'] / 5))), (self.current_settings['DividerSmall'] * floor((self.current_settings['LineWidthLimit'] / 7))))
            default_settings_str,current_settings_str='',''
            for dsi in self.default_settings:
                iname,ivalue=dsi,self.default_settings[dsi]
                default_settings_str+='  ->' + iname + ': ' + value + '\n'
            for csi in self.current_settings:
                iname,ivalue=dsi,self.current_settings[csi]
                current_settings_str+='  ->' + iname + ': ' + value + '\n'
            output_text_str=top_display + "DEFAULT SETTINGS:\n{}\nCURRENT SETTINGS:\n{}".format(default_settings_str,current_settings_str)
            return self.__width_limit_fmt(print_str=output_text_str)
        def BookmarksBar_display(self):
            output_text_str="\n{} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} BOOKMARKS\n{}(INPUT TO EXIT BACK TO HOME--> B)".format((self.current_settings['DividerLarge'] * floor((self.current_settings['LineWidthLimit'] / 3))), (self.current_settings['DividerMedium'] * floor((self.current_settings['LineWidthLimit'] / 5))), (self.current_settings['DividerSmall'] * floor((self.current_settings['LineWidthLimit'] / 7))))
            for bki in self.bookmarks:
                output_text_str+="  ->{} | {}\n".format(bki,self.bookmarks[bki]['name'])
             return self.__width_limit_fmt(print_str=output_text_str)
        def PrintContents_display(self):
            top_str="\n{}\nDEVELOPER TOOLKIT:\n{}\nCONTENTS DISPLAY FOR FILE OR FOLDER\n{}\n".format(self.dividers['DividerLarge'],self.dividers['DividerMedium'],self.dividers['DividerSmall'])
            cwd_contents="CONTENTS:\n" + Path(self.CLI_cwd).read_text().split('\n')
            cwd_contents_str=''
            for conti in cwd_contents:
                cwd_contents_str+=conti + '\n'
            return self.__width_limit_fmt(print_str=top_str + cwd_contents_str)
        def PrintPreview_display(self):
            top_str="\n{}\nDEVELOPER TOOLKIT:\n{}\nPREVIEW DISPLAY FOR FILE OR FOLDER\n{}\n".format(self.dividers['DividerLarge'],self.dividers['DividerMedium'],self.dividers['DividerSmall'])
            if os.path.isfile(self.CLI_cwd):
                cwd_contents=Path(self.CLI_cwd).read_text().split('\n')[0:self.current_settings['PreviewLineHeightLimit']]
            else:
                cwd_contents=['\nSUB-DIRECTORIES:\n']
                subdirs_list, files_list=[],[]
                for diri in os.listdir():
                    diri_str='  ->' + diri + ' | PATH: ' + os.path.abspath(diri) +'\n'
                    if os.path.isfile(diri):
                        files_list.append(diri_str)
                    else:
                        subdirs_list.append(diri_str)]
                for sdli in subdirs_list:
                    cwd_contents.append(sdli)
                cwd_contents.append('\nFILES IN FOLDER:\n')
                for flli in files_list:
                    cwd_contents.append(flli)
            cwd_contents_str=''
            for conti in cwd_contents:
                cwd_contents_str+=conti + '\n'
            return self.__width_limit_fmt(top_str + cwd_contents_str)
        def execStringInput_display(self):
            exec_display_str="\n{} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} MANUAL OVERRIDE MODE exec() CALL\n{}\nNOW RUNNING: \n exec(\n".format(self.dividers['DividerLarge'],self.dividers['DividerMedium'],self.dividers['DividerSmall'])
            exec_display_str+=self.exec_str + ')\n'
            return self.__width_limit_fmt(exec_display_str)

        ###############################
        ### COMMAND LOGIC FUNCTIONS ###
        ###############################
        def TeleportToSpecifiedPath(self,to_path,print_preview_not_contents=True):
            self.back_button_paths=[self.CLI_cwd] + self.back_button_paths[:-1]
            self.forward_button_paths=[]
            self.CLI_cwd=to_path
            self.__update_usage_data(self.CLI_cwd)
            self.CLI_mode='PrintPreview' if print_preview_not_contents else 'PrintContents'
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def NavigateBack(self):
            if len(self.forward_button_paths)==len([]):
                nowhere_to_navigate_back_error_str="ERROR! The interface has not stored any valid directories for the back button to navigate to as of yet."
                print(nowhere_to_navigate_forward_error_str)
            else:
                to_path=self.back_button_paths[0]
                self.back_button_paths=self.back_button_paths[1:]
                self.forward_button_paths=[self.CLI_cwd] + self.forward_button_paths[:-1]
                self.CLI_cwd=to_path
                self.__update_usage_data(self.CLI_cwd)
                self.CLI_mode='PrintPreview'
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def NavigateForward(self):
            if len(self.forward_button_paths)==len([]):
                nowhere_to_navigate_forward_error_str="ERROR! The interface has not stored any valid directories for the forward button to navigate to as of yet."
                print(nowhere_to_navigate_forward_error_str)
            else:
                to_path=self.forward_button_paths[0]
                self.back_button_paths=self.forward_button_paths self.back_button_paths[]
                self.forward_button_paths=self.forward_button_paths[]
                self.CLI_cwd=to_path
                self.__update_usage_data(self.CLI_cwd)
                self.CLI_mode='PrintPreview'
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def ParentDirectory(self):
            parent_path=Path(self.CLI_cwd).parent.absolute()
            self.back_button_paths=[self.CLI_cwd] + self.back_button_paths[:-1]
            self.forward_button_paths=[]
            self.CLI_cwd=parent_path
            self.__update_usage_data(self.CLI_cwd)
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def PrintPreview(self,to_path):
            self.__TeleportToSpecifiedPath(to_path)
        def PrintContents(self,to_path):
            if os.path.isfile(self.CLI_cwd):
                self.__TeleportToSpecifiedPath(to_path, print_preview_not_contents=False)
            else:
                no_printable_contents_error_str="Error! The current CLI windows path is not available for viewing, only previewing. Likely this is due to the windows path being set to a folder and not a file."
                print(no_printable_contents_error_str)
        def ReturnToHomePage(self):
            self.CLI_mode='Home'
            self.back_button_paths=self.back_button_paths[]
            self.forward_button_paths=self.forward_button_paths[]
            self.CLI_cwd=self.src_dir_path
            self.__update_usage_data(self.CLI_cwd)
        def ToggleHelpMenuDisplay(self):
            self.CLI_mode='Help' if self.CLI_mode!='Help' else 'PrintPreview'
        def ToggleSettingsDisplay(self):
            self.CLI_mode='Settings' if self.CLI_mode!='Settings' else 'PrintPreview'
        def ResetSettingsToDefaults(self):
            self.current_settings=self.default_settings
        def ToggleSettingsValue(self, setting_name, change_value_to_this):
            self.current_settings[setting_name]=change_value_to_this
            if self.current_settings['RESET_TO_DEFAULT']:
                self.__ResetSettingsToDefaults()
        def OpenBookmarksBar(self):
            self.CLI_mode='Bookmarks'
        def SaveCurrentPathAsBookmark(self):
            print("Please input name for the new bookmark of path: {}".format(self.CLI_cwd))
            bookmark_name=input()
            if self.CLI_cwd in [k for k in self.usage_count]:
                usage_ct=self.usage_count[self.CLI_cwd]
            else:
                usage_ct=0
            self.bookmarks[self.CLI_cwd]={'name':bookmark_name,'bookmark_usage_count':usage_ct}
        def OpenBookmark(self,name_or_path):
            if name_or_path in self.bookmarks:
                to_path=self.bookmark[name_or_path]
                self.__TeleportToSpecifiedPath(to_path)
            elif name_or_path in [self.bookmarks[k]['name'] for k in self.bookmarks]:
                for k in self.bookmarks:
                    if self.bookmarks[k]['name']==name_or_path:
                        to_path=self.bookmarks[k]['name']
                self.__TeleportToSpecifiedPath(to_path)
            else:
                bookmark_not_found_error_str="""
                Error! No bookmarks exist specified by name_or_path input: {}
                """.format(name_or_path)
                print(bookmark_not_found_error_str)
        def execStringInput(self, exec_file_path_or_str):
            if os.path.exists(exec_file_path_or_str) and exec_file_path_or_str.endswith('.txt'):
                with open(exec_file_path_or_str, 'r') as opentxt:
                    exec_str=opentxt.read()
            else:
                exec_str=exec_file_path_or_str
            self.exec_str=exec_str

        ###############################
        ### CLI SHUTDOWN OPERATIONS ###
        ###############################
        def __save_new_metadata_to_files(self):
            with open(self.usage_data_path,"w") as outfile:
                json.dump(self.usage_data,outfile)
            with open(self.bookmarks_path,"w") as outfile:
                json.dump(self.default_settings,outfile)
            with open(self.current_settings_path,"w") as outfile:
                json.dump(self.current_settings,outfile)
            with open(self.cmd_metadata_path,"w") as outfile:
                json.dump(self.cmd_metadata,outfile)
        def __save_session_log_as_txt(self):
            combined_str=''
            for stri in self.session_log['saved_str_blocks']:
                combined_str+='\n' + stri
            with open(self.session_log_path,"w") as sessiontxt:
                sessiontxt.write(combined_str)
        def ExitCLI(self):
            self.session_log['timestamps'][1]=str(time.time())
            self.session_log_path=self.src_dir_path + self.sys_slashes + 'session_from_{}_to_{}.txt'.format(self.session_log['timestamps'][0],self.session_log['timestamps'][1]) + self.sys_slashes
            self.__update_usage_data_for_bookmarks_dicts()
            self.__save_new_metadata_to_files()
            self.__save_session_log_as_txt()
            self.POWER=False

        ############
        ### INIT ###
        ############
        def init__(
                   self,
                   src_dir_path=src_dir_path,
                   jump_to_path=jump_to_path,
                   width_limit=width_limit,
                   height_limit=height_limit,
                   manual_override_pwd=manual_override_pwd,
                   author=author,
                   version=version,
                   created=created,
                   **kwargs
                  ):

            ###############
            ### METHODS ###
            ###############
            self.__os_syntax_profiling()
            self.__establish_paths(src_dir_path)
            self.__load_bookmarks()
            self.__load_usage_data()
            self.__load_cmd_metadata()
            self.__load_default_settings()
            self.__load_current_settings()
            self.__check_manual_override_credentials(manual_override_pwd)
            self.__proportioned_divider_strs()
            self.__get_all_valid_commands_for_current_windows()

            ##################
            ### ATTRIBUTES ###
            ##################
            self.session_log={'timestamps':[str(time.time()), None],'saved_str_blocks':[]}
            self.about={'Author':author,'Version':version,'Created':created}
            self.width_limit=width_limit
            self.height_limit=height_limit
            self.manual_override_pwd=manual_override_pwd
            self.CLI_cwd=(self.current_settings['HomePathString']) if (jump_to_path is None) else jump_to_path
            self.CLI_mode='Home'
            self.back_button_paths=[]
            self.forward_button_paths=[] # !!! NOTE: 0 INDEX IS MOST RECENT FOR NAVIGATION CACHES !!!
            self.exec_str=''
            self.user_input_dict={}

        ################
        ### CLI LOOP ###
        ################
        def CLI_display():
            # TOP
            if self.current_settings['StatusBarPosition']=='top':
                status_bar_str=self.__status_bar_display()
                self.__update_txt_session_log(status_bar_str)
                print(status_bar_str)
            else:
                divider_line=self.dividers['DividerSmall'] + '\n' + self.dividers['DividerMedium'] + '\n' + self.dividers['DividerLarge']
                self.__update_txt_session_log(divider_line)
                print(divider_line)
            if self.current_settings['PrintInterfaceMetadata']:
                interface_metadata_str="\n{}\nCLI_cwd: {}\nCLI_mode: {}\nuser_input: {}\n{}\n".format(self.dividers['DividerMedium'],self.CLI_cwd, self.CLI_mode, self.user_input_dict,self.dividers['DividerMedium'])
                interface_metadata_str=self.__width_limit_fmt(interface_metadata_str)
                self.__update_txt_session_log(interface_metadata_str)
                print(interface_metadata_str)
            # MID
            if self.CLI_mode is 'Home':
                save_and_print_me=self.__home_page()
            elif self.CLI_mode is 'Help':
                save_and_print_me=self.__help_display()
            elif self.CLI_mode is 'Settings':
                save_and_print_me=self.__settings_display()
            elif self.CLI_mode is 'Bookmarks':
                save_and_print_me=self.__bookmarks_bar_display()
            elif self.CLI_mode is 'execFileContents':
                save_and_print_me=self.__file_exec_str_display()
            elif os.path.exists(self.CLI_cwd):
                if self.CLI_mode='PrintPreview':
                    self.__print_preview_display()
                elif self.CLI_mode='PrintContents' and (not os.path.isfile(self.CLI_cwd)):
                    self.__print_contents_display()
            else:
                save_and_print_me="ERROR! DTK_CLI.CLI_cwd does not point to a valid page for the command line interface to display. In the worst case, please restart the program."
            self.__update_txt_session_log(save_and_print_me)
            print(save_and_print_me)
            # LOW
            if self.current_settings['StatusBarPosition']=='bottom':
                status_bar_str=self.__status_bar_display()
                self.__update_txt_session_log(status_bar_str)
                print(status_bar_str)
            else:
                divider_line=self.dividers['DividerSmall'] + '\n' + self.dividers['DividerMedium'] + '\n' + self.dividers['DividerLarge']
                self.__update_txt_session_log(divider_line)
                print(divider_line)
            # MISC
            if self.CLI_mode is 'execFileContents':
                print_exec_str=self.exec_str
                self.exec_str=''
                exec(print_exec_str)
        def CLI_cmd(input_cmd_str):
            self.user_input_dict=self.__user_input_cmd_compiler(input_cmd_str)
            if self.user_input_dict['parameters'] != {}:
                fn_inputs=''
                for paramsi in [prmi for prmi in self.user_input_dict['parameters']]:
                    fn_inputs+=paramsi + '=' + self.user_input_dict['parameters'][paramsi]['input_arg'] + ','
            else:
                fn_inputs=''
            while fn_inputs.endswith(','):
                fn_inputs = fn_inputs[:-1]
            input_cmd_name=self.user_input_dict['cwd_name']
            exec('self.__{}({})'.format(input_cmd_name, fn_inputs))

        def initiate_interface(self):
            self.POWER=True
            while self.POWER:
                os.chdir(self.CLI_cwd)
                self.__CLI_display()
                CLI_input=input()
                self.__CLI_cmd(CLI_input_cmd)

    #################################################
    ### FORM OBJECT INSTANCE AND EXECUTE CLI LOOP ###
    #################################################
    dtk_cli=DEVELOPER_TOOLKIT_COMMAND_LINE_INTERFACE()
    dtk_cli.__initiate_interface_loop()

################################################################
### main() FUNCTION CALLED VIA OPENING FILE THROUGH TERMINAL ###
################################################################
if __name__=='__main__':
    main()
