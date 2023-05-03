#####################################################################
### dtk-cli.py -- DEVELOPER TOOLKIT COMMAND LINE INTERFACE OBJECT ###
#####################################################################
__author__="Eamon Smith (github.com/33aquarius)"
__version__='1.0'
__created__='4/3/2023'
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
import time
import inspect
#########################
### DATA MANIPULATION ###
#########################
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import csv
import string
from textwrap import wrap
############
### MISC ###
############
import webbrowser
import hashlib
from hashlib import sha256
import math
from math import floor, ceil
#######################
### main() FUNCTION ###
#######################
def main(author=__author__, version=__version__, created=__created__):
    ################
    ### ARGPARSE ###
    ################
    def ARGPARSE_CONDENSER():
        parser=argparse.ArgumentParser()
        parser.add_argument('-fp','--file-path',dest='filepath',metavar='file path',help='Direct path input to access desired dev-toolkit function.', required=False, default=os.getcwd())
        parser.add_argument('-hp','--home-path',dest='homepath',metavar='home path',help='Sets the home path for the command line interface. Default == the directory containing the dtk-cli.py file.', required=False, default=os.getcwd())
        parser.add_argument('-wl','--width-limit', dest='width_limit',metavar='number',help='Sets the character limit per line in the command line interface. This must be an integer! Default == 133.',required=False,default=133)
        parser.add_argument('-lc','--height-limit', dest='height_limit',metavar='number',help='Sets the maximum number of lines that can be taken up by the contents of a file being previewed. This must be an integer! Default == 24.',required=False,default=69)
        parser.add_argument('-sm','--start-mode',dest='startmode',metavar='str',help='Specifies the CLI mode upon launch. Default: home',required=False,default='home')
        parser.add_argument('-MO','--manual-override-pwd',dest='manual_override_pwd',help='Dev argument to access more functionality. This method means nothing without inputting the correct password, which == cross-referenced with a pre-generated hash output.', required=False, default=None)
        args=parser.parse_args()
        return args
    args=ARGPARSE_CONDENSER()
    ###############################
    ## FUNCTIONALITY CORE CLASS ###
    ###############################
    class FN_CORE:
        def __os_syntax_profiling(self):
            platforms={'linux1':'linux','linux2':'linux','darwin':'os_x','win32':'windows'}
            slashes={'linux':'/','windows':r'\\','os_x':'/'}
            sys_os=sys.platform if sys.platform not in platforms else platforms[sys.platform]
            sys_slashes=slashes['linux'] if sys_os not in slashes else slashes[sys_os] # assume linux syntax for slashes used in path strs
            return sys_os, sys_slashes
        def __establish_paths(self,src_dir_path=None):
            src_dir_path=args.homepath if src_dir_path == None else os.getcwd()
            sys.path.append(src_dir_path)
            return src_dir_path
        def __fetch_desktop_path(self):
            desktop_path=(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) # may encounter difficulties if the DTK-CLI folder == not located somewhere on desktop, thus doing so == recommended for ease of use. Otherwise, you will need to pass something else though here.
            return desktop_path
        def __check_manual_override_credentials(self,manual_override_pwd):
                if manual_override_pwd==None:
                    correct_pwd_entered = False
                else:
                    manual_override_pwd_hash=hashlib.sha256(manual_override_pwd.encode()).hexdigest()
                    reference_hash="6f943458264a2e5b9136549a82127f03c161bd91afbe0f93e807e35f9cb1e7ca"
                    correct_pwd_entered=True if (manual_override_pwd==reference_hash) else False
                    if not correct_pwd_entered:
                        print("ERROR: THE CORRECT STRING FOR THE INPUT ARGUMENT manual_override_pwd WAS NOT PASSED. THE PROGRAM WILL STILL LAUNCH, BUT FUNCTIONALITIES PERTAINING TO 'MANUAL OVERRIDE MODE' WILL BE INACCESSIBLE.")
                return correct_pwd_entered
        def __init__(
                     self,
                     src_dir_path=args.homepath,
                     manual_override_pwd=args.manual_override_pwd,
                     author=__author__,
                     version=__version__,
                     created=__created__
                    ):
            self.author=author
            self.version=version
            self.created=created
            self.about={'author':self.author,'version':self.version,'created':self.created}
            self.sys_os, self.sys_slashes=__os_syntax_profiling()
            self.src_dir_path=__establish_paths(src_dir_path)
            self.manual_override_mode=self.__check_manual_override_credentials(manual_override_pwd)
    ########################
    ## LOAD HELPER CLASS ###
    ########################
    class LoadHelper__DTK_CLI(FN_CORE):
        def __load_bookmarks(self):
            if os.path.isfile(self.bookmarks_path):
                with open(self.bookmarks_path, "r") as iter_json_to_load:
                    bookmarks=json.load(iter_json_to_load)
            else:
                bookmarks={(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')):{'name':'Desktop','bookmark_usage_count':0},
                             src_dir_path:{'name':'Toolkit home','bookmark_usage_count':0}}
                with open(self.bookmarks_path, "w") as outfile:
                    json.dump(bookmarks, outfile)
            return bookmarks
        def __load_usage_data(self):
            if os.path.isfile(self.usage_data_path):
                with open(self.usage_data_path, "r") as iter_json_to_load:
                    usage_data=json.load(iter_json_to_load)
            else:
                usage_data={__fetch_desktop_path():0,
                            self.src_dir_path:0}
                with open(self.usage_data_path, "w") as outfile:
                    json.dump(usage_data, outfile)
            return usage_data
        def __load_default_settings(self):
            if os.path.isfile(self.default_settings_path):
                with open(self.default_settings_path, "r") as iter_json_to_load:
                    default_settings=json.load(iter_json_to_load)
            else:
                default_settings={
                                  'homePathString':self.src_dir_path,
                                  'DesktopPathString':(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')),
                                  'WidthLimit':width_limit,
                                  'HeightLimit':height_limit,
                                  'FixSentenceEndings':True,
                                  'TabSizeDivisor':10,
                                  'Divider_XXL':'X',
                                  'Divider_XXL_proportion':1,
                                  'Divider_XL':'X',
                                  'Divider_XL_proportion':1.33,
                                  'Divider_L':'X',
                                  'Divider_L_proportion':2.22,
                                  'Divider_M':'~',
                                  'Divider_M_proportion':3.33,
                                  'Divider_S':'-',
                                  'Divider_S_proportion':4.44,
                                  'Divider_XS':'-',
                                  'Divider_XS_proportion':6.66,
                                  'Divider_XXS':'-',
                                  'Divider_XXS_proportion':6.66,
                                  'StatusBarDateTimeFormat':"%H:%M:%S",
                                  'StatusBarPosition':'bottom', # 'top' or 'bottom'
                                  'TimeZone':datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo,
                                  'PrintInterfaceMetadata':True,
                                  'ManualOverridePwd':manual_override_pwd,
                                  'RESET_TO_DEFAULT':False
                                 }
                with open(self.default_settings_path, "w") as outfile:
                    json.dump(default_settings, outfile)
            return default_settings
        def __load_current_settings(self):
            current_settings={}
            if os.path.isfile(self.current_settings_path):
                with open(self.current_settings_path, "r") as iter_json_to_load:
                    current_settings=json.load(iter_json_to_load)
            else:
                current_settings=__load_default_settings()
                with open(self.current_settings_path, "w") as outfile:
                    json.dump(current_settings, outfile)
            return current_settings
        def __load_cmd_metadata():
        self.cmd_metadata_path=self.src_dir_path + self.sys_slashes +  'commands.json'
        if os.path.isfile(self.cmd_metadata_path):
            with open(self.cmd_metadata_path, "r") as iter_json_to_load:
                commands_metadata=json.load(iter_json_to_load)
        else:
            command_parameters={
                                'Setting':{'CLI_syntax':'--s',
                                           'description':'This parameter == used to specify the parameter whose value we want to change when we are adjusting CLI settings.'},
                                'Value':{'CLI_syntax':'--v',
                                         'description':'This parameter == used to specify any value used in the command.'},
                                'Path':{'CLI_syntax':'--p',
                                        'description':'This parameter == used to specify the strings for any paths used in the command.'},
                                'Name':{'CLI_syntax':'--n',
                                        'description':'This parameter == used to specify the name of any object during command execution.'},
                                'ID':{'CLI_syntax':'--id',
                                      'description':'This parameter denotes either the name or the path of what is being specified in the command (ex. a bookmark).'},
                                'Bookmark':{'CLI_syntax':'--b',
                                            'description':'This parameter can either be the name of a bookmark or the string of the path for the bookmark. The CLI will automatically process both.'},
                                'execManualStr':{ 'CLI_syntax':'--exs',
                                                 'description':'This parameter can specify either the path of a .txt file which contains the string of code which will be run via exec(). The parameter can also just be the string to be passed through exec() as well--the CLI will attempt to distinguish this by checking if the string == a valid path.'}
                               }
            command_parameters_names_list=[cmdp for cmdp in command_parameters]
            command_parameters_syntax_list=[command_parameters[prmni]['CLI_syntax'] for prmni in command_parameters_names_list]
            global_commands={
                             'ExitCLI':{'description':'Exit the toolkit command line interface.',
                                        'CLI_syntax':'X',
                                        'allowed_variations':['ExitCLI','x','X','exit()','exit','EXIT','esc','ESC','/exit','/EXIT','/X','/x','x()','X()'], # references allowed variations for input arguments to trigger this command
                                        'correlated_cmd_method_names_list':['']
                                        'allowed_params_list':['']},
                             'ReturnToHomePage':{'description':'Return to the home view on the CLI',
                                                 'CLI_syntax':'H',
                                                 'allowed_variations':['ReturnToHomePage','h','H','home','home','/home','home()','/h','/H'],
                                                 'correlated_cmd_method_names_list':['']},
                             'ToggleHelpMenuDisplay':{'description':'Opens/closes up the help menu on the CLI.',
                                                   'CLI_syntax':'?',
                                                   'allowed_variations':['ToggleHelpMenuDisplay','?', 'Help','HELP','/help','/?','/h','/H','/HELP','help()'],
                                                   'correlated_cmd_method_names_list':['']},
                             'ToggleSettingsDisplay':{'description':'Opens/closes up the settings menu.',
                                                      'CLI_syntax':'S',
                                                      'allowed_variations':['Settings','S','s','/settings','SETTINGS','/S','/s', 'settings()'],
                                                      'correlated_cmd_method_names_list':['']},
                             'ToggleSettingValue':{'description': 'Allows for any of the values in the settings to be adjusted. These commands can also be triggered outside of the settings menu itself.',
                                                   'CLI_syntax':'S --s [PARAMETER] --v [VALUE]',
                                                   'allowed_variations':['SETTINGS --p [PARAMETER] --v [VALUE]', 'S --p [PARAMETER] --v [VALUE]', 'settings([PARAMETER], [VALUE])', '/settings [PARAMETER] [VALUE]'],
                                                   'correlated_cmd_method_names_list':['']},
                             'OpenBookmarksBar':{'description':'Opens the bookmarks bar window, where either default or previous bookmarks are loaded for access.',
                                                 'CLI_syntax':'BK',
                                                 'allowed_variations':['OpenBookmarksBar','/OpenBookmarksBar','OpenBookmarksBar()','BOOKMARKS','BK','Bookmarks','bk','bookmarks()','','','',''],
                                                 'correlated_cmd_method_names_list':['']},
                             'OpenBookmark':{'description':'Opens the bookmark specified by the name of the bookmark or the path of the bookmark.',
                                             'CLI_syntax':'OB --',
                                             'allowed_variations':[],
                                             'correlated_cmd_method_names_list':['']}
            }
            path_specific_commands={
                             'TeleportToSpecifiedPath':{'description':'Shifts the CLI window to a view at the path str or the name of the file. This ideally == the full path str.',
                                                       'CLI_syntax':'BK',
                                                       'allowed_variations':['TeleportToSpecifiedPath --id [ID]','/TeleportToSpecifiedPath --id [ID]', 'TP --id [ID]','tp --id [ID]', 'chdir --id [ID]', 'cd --id [ID]', 'cd --id [ID]', '/tp PATH', '/tp --id [ID]','/TP --id [ID]','/TP --id [ID]','teleport(--id [ID])','tp(--id [ID])'],
                                                       'correlated_cmd_method_names_list':['']},
                             'NavigateForward':{'description':'The same as a forward button on a web browser.',
                                                'CLI_syntax':'>',
                                                'allowed_variations':['Foward','f','F','forward','FORWARD', '>','forward()','/forward','/f'],
                                                'correlated_cmd_method_names_list':['']},
                             'NavigateBack':{'description':'The same as a back button on a web browser.',
                                             'CLI_syntax':'<',
                                             'allowed_variations':['Back','B', 'back','b', ' BACK', '<','back()','/back','/b'],
                                             'correlated_cmd_method_names_list':['']},
                             'ParentDirectory':{'description':'Moves the interface window path to the to the parent of the current directory.',
                                                'CLI_syntax':'PD',
                                                'allowed_variations':['ParentDirectory','/ParentDirectory','P','p','parent','PARENT','..','<<','parent()','/p','/parent','/P','parent()'],
                                                'correlated_cmd_method_names_list':['']},
                             'PrintContents':{'description':'Prints the contents of the file within the command line interface. This method removes all formatting with regard to width specifications to maintain the original layout of the file.',
                                              'CLI_syntax':'PFC',
                                              'allowed_variations':['PrintFileContents','/PrintFileContents', 'PF-C','PrintFileContents()','Contents()','pf-c','/PF-C','/pf-c'],
                                              'correlated_cmd_method_names_list':['']},
                             'PrintPreview':{'description':'Prints a preview of the contents of a file, which has a max line count of the -lc (--preview-height) parameter. Depending on the file, this summary may be more detailed than just the first height_limit lines of a file.',
                                             'CLI_syntax':'PFP',
                                             'allowed_variations':['PrintFilePreview','pf-p','PREVIEW','PF-P','Preview()','PrintFilePreview()','/pf-p','/PF-P','/preview','/PREVIEW','/PrintFilePreview'],
                                             'correlated_cmd_method_names_list':['']},
                             'SaveCurrentPathAsBookmark':{'description':'Saves the directory path associated with the current interface window as a bookmark. Running this command will prompt a second input for the bookmark name unless it == also specified in the first call.',
                                                          'CLI_syntax':'SBK --n [NAME]',
                                                          'allowed_variations':['SaveCurrentPathAsBookmark --n [NAME]','/SaveCurrentPathAsBookmark --n [NAME]','SaveCurrentPathAsBookmark([NAME])','SBK --n [NAME]','/SBK --n [NAME]','SBK([NAME])','sbk --n [NAME]','/sbk --n [NAME]','sb([NAME])'],
                                                          'correlated_cmd_method_names_list':['']},
            }
            EXEC_WARNING_TEXT='Only available with manual override. WARNING: THIS FUNCTION IS VERY DANGEROUS. MAKE SURE YOU KNOW EXACTLY WHAT YOU ARE PASSING THROUGH EXEC().'
            manual_commands={'execStringInput':{'description':(EXEC_WARNING_TEXT + '\nThe interface will prompt another input upon calling this command, and the str next inputted by the user will be passed through the exec() function (native to python). The methods of calling the command involving [TXT_PATH] refer to the path of a .txt file containing the str which can be passed through exec() (this removes limitations for being limited to a single line of code).'),
                                                'CLI_syntax':'execStringInput',
                                                'allowed_variations':['execStringInput','/execStringInput','execStringInput()', 'execStringInput --txt [TXT_PATH]','/execStringInput --txt [TXT_PATH]','execStringInput([TXT_PATH])'],
                                                'correlated_cmd_method_names_list':['']}}
            global_commands_names_list,path_specific_commands_names_list,manual_commands_names_list=[gci for gci in global_commands],[pci for pci in path_specific_commands],[mci for mci in manual_commands]
            global_commands_syntax_list,path_specific_commands_syntax_list,manual_commands_syntax_list=[global_commands[gci]['CLI_syntax'] for gci in global_commands_names_list],[path_specific_commands[gci]['CLI_syntax'] for pci in path_specific_commands_names_list],[manual_commands[gci]['CLI_syntax'] for mci in manual_commands_names_list]
            total_commands_names_list=global_commands_names_list+path_specific_commands_names_list+manual_commands_names_list
            total_commands_syntax_list=global_commands_syntax_list+path_specific_commands_syntax_list+manual_commands_syntax_list
            name_syntax_lists={
                               'global_names':global_commands_names_list,
                               'global_syntax':global_commands_syntax_list,
                               'path_specific_names':path_specific_commands_names_list,
                               'path_specific_syntax':path_specific_commands_syntax_list,
                               'manual_names':manual_commands_names_list,
                               'manual_syntax':manual_commands_syntax_list,
                               'total_names':total_commands_names_list,
                               'total_syntax':total_commands_syntax_list,
                               'param_names':command_parameters_names_list,
                               'param_syntax':command_parameters_syntax_list,
                              }
            commands_metadata={
                               'command_parameters':command_parameters,
                               'global_commands':global_commands,
                               'path_specific_commands':path_specific_commands,
                               'manual_commands':manual_commands,
                               'names_and_syntax':name_syntax_lists
                               }
            with open(self.cmd_metadata_path, "w") as outfile:
                json.dump(commands_metadata, outfile)
        return commands_metadata
        def __load_dividers(self):
            divider_proportions={
                                 'Divider_XXL':self.current_settings['Divider_XXL_proportion'],
                                 'Divider_XL':self.current_settings['Divider_XL_proportion'],
                                 'Divider_L':self.current_settings['Divider_L_proportion'],
                                 'Divider_M':self.current_settings['Divider_M_proportion'],
                                 'Divider_S':self.current_settings['Divider_S_proportion'],
                                 'Divider_XS':self.current_settings['Divider_XS_proportion'],
                                 'Divider_XXS':self.current_settings['Divider_XXS_proportion']
                                }
            proportioned_XXL=(self.current_settings['Divider_XXL'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_XXL'])))
            proportioned_XL=(self.current_settings['Divider_XL'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_XL'])))
            proportioned_L=(self.current_settings['Divider_L'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_L'])))
            proportioned_M=(self.current_settings['Divider_M'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_M'])))
            proportioned_S=(self.current_settings['Divider_S'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_S'])))
            proportioned_XS=(self.current_settings['Divider_XS'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_XS'])))
            proportioned_XXS=(self.current_settings['Divider_XXS'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['Divider_XXS'])))
            proportioned_output_dividers={
                                          'Divider_XXL':{'unit':self.current_settings['Divider_XXL'],
                                                            'proportioned':proportioned_XXL},
                                          'Divider_XL':{'unit':self.current_settings['Divider_XL'],
                                                            'proportioned':proportioned_XL},
                                          'Divider_L':{'unit':self.current_settings['Divider_L'],
                                                            'proportioned':proportioned_L},
                                          'Divider_M':{'unit':self.current_settings['Divider_M'],
                                                             'proportioned':proportioned_M},
                                          'Divider_S':{'unit':self.current_settings['Divider_S'],
                                                            'proportioned':proportioned_S},
                                          'Divider_XS':{'unit':self.current_settings['Divider_XS'],
                                                            'proportioned':proportioned_XS},
                                          'Divider_XXS':{'unit':self.current_settings['Divider_XXS'],
                                                            'proportioned':proportioned_XXS}
                                         }
            return proportioned_output_dividers
        def __init__(
                     self,
                     jump_to_path=args.filepath,
                     jump_to_mode=args.startmode,
                     width_limit=args.width_limit,
                     height_limit=args.height_limit,
                     start_mode=args.startmode,
                     **kwargs
                    ):
            self.POWER=True
            self.width_limit=width_limit
            self.height_limit=height_limit
            self.start_mode=start_mode
            self.bookmarks_path=self.src_dir_path + self.sys_slashes + 'bookmarks.json'
            self.usage_data_path=self.src_dir_path + self.sys_slashes + 'usage_data.json'
            self.default_settings_path=self.src_dir_path + self.sys_slashes + 'default_settings.json'
            self.current_settings_path=self.src_dir_path + self.sys_slashes + 'current_settings.json'
            self.cmd_metadata_path=self.src_dir_path + self.sys_slashes +  'commands.json'
            super().__init__(**kwargs)
    ##########################
    ## METHOD HELPER CLASS ###
    ##########################
    class MethodHelper__DTK_CLI(LoadHelper__DTK_CLI):
        def __obtain_fmt_datetime_as_str(self,unix_time_or_now='now',time_zone=None):
            time_zone = (self.current_settings['TimeZone'] if time_zone == None) else time_zone
            return_datetime_str=''
            if 'current_settings' in dir(self):
                strftime_fmt = self.current_settings['StatusBarDateTimeFormat']
            else:
                strftime_fmt = '%Y-%m-%d %H:%M:%S'
            if unix_time_or_now=='now':
                return_datetime_str=datetime.utcfromtimestamp(time.time()).astimezone(time_zone).strftime(strftime_fmt)
            elif (isinstance(unix_time_or_now), int) or (isinstance(unix_time_or_now, float)):
                return_datetime_str=datetime.utcfromtimestamp(unix_time_or_now).strftime(strftime_fmt)
            else:
                bad_ftm_for_time_input_error_str="""
                ERROR! DATETIME CANNOT BE DISPLAYED PROPERLY. PLEASE REFERENCE DTK_CLI.__obtain_fmt_datetime_as_str() FOR DETAILS.
                """
                print(bad_ftm_for_time_input_error_str)
                return_datetime_str='DATETIME ERROR'
            return return_datetime_str
        def __open_url_on_client_browser(self,url_str, new=0, autoraise=True, **kwargs):
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
        def __print_divider_sequences_easily(self, divider_ids_iterable=[], new_line_before=True,new_line_after=True,piano_range_and_step=[]): # specify with tag sizes--'XL', 'S', etc. piano_range_and_step must be a 3-element iterable [range_start, range_end, step]
            printed_divider_sequence_str='' if not new_line_before else '\n'
            if divider_ids_iterable==[] and piano_range_and_step==[]:
                invalid_input_error_string='ERROR! INPUT CRITERIA FOR ARGS divider_ids_iterable AND piano_range_and_step WITHIN DTK_CLI.__print_divider_sequences_easily(). BOTH CANNOT BE EMPTY!'
        def __obtain_command_classification(self,cmd_name_or_syntax):
            cmd_is_name = True if (cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['total_names']) else False
            output_classification=''
            if cmd_is_name:
                if cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['global_names']:
                    output_classification='global'
                elif cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['path_specific_names']:
                    output_classification='path_specific'
                elif cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['global_names']:
                    output_classification='manual'
            else:
                if cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['global_syntax']:
                    output_classification='global'
                elif cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['path_specific_syntax']:
                    output_classification='path_specific'
                elif cmd_name_or_syntax in self.cmd_metadata['names_and_syntax']['global_syntax']:
                    output_classification='manual'
            return output_classification
        def __get_all_valid_commands_for_current_windows(self):
            output_valid_commands_dict=(self.cmd_metadata['manual_commands']) if self.CLI['manual_override_mode'] else {}
            global_commands_dict=self.cmd_metadata['global_commands']
            path_specific_commands_dict=self.cmd_metadata['path_specific_commands']
            for cmdi in global_commands_dict:
                output_valid_commands_dict[cmdi]=self.cmd_metadata['global_commands'][cmdi]
            for cmdi in path_specific_commands_dict:
                if cmdi in ['TeleportToSpecifiedPath', 'NavigateForward', 'NavigateBack','ParentDirectory','SaveCurrentPathAsBookmark']:
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_specific_commands'][cmdi]
                elif cmdi=='PrintPreview' and (self.CLI['mode']=='PrintContents'):
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_specific_commands'][cmdi]
                elif cmdi=='PrintContents' and self.CLI['mode']=='PrintPreview':
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_specific_commands'][cmdi]
            return output_valid_commands_dict
        def __update_txt_session_log(self, str_block_to_append_to_agg):
            session_log_list=[]
            if hasattr(self,'session_log') and isinstance(self.session_log['saved_str_blocks'], list):
                session_log_list=self.session_log['saved_str_blocks']
                session_log_list.append(str_block_to_append_to_agg)
                session_log=self.session_log
                session_log['saved_str_blocks']=session_log_list
            else:
                session_log_list=[str_block_to_append_to_agg]
                session_log={'timestamps':[str(time.time()), None],'saved_str_blocks':session_log_list}
            self.session_log=session_log
        def __update_usage_data(self, path_accessed):
            if path_accessed in [udk for udk in self.usage_data]:
                self.usage_data[path_accessed]+=1
            else:
                self.usage_data[path_accessed]=1
            for bookmarks_iter in self.bookmarks:
                self.bookmarks[bookmarks_iter]['bookmark_usage_count']=self.usage_data[bookmarks_iter]
        def __trim_navigate_forwards_or_backwards_path_history_lists(self):
            cache_size_limit=self.current_settings['NavigationCacheSizeLimit']
            if len(self.CLI['back_cache']) > cache_size_limit:
                while len(self.CLI['back_cache']) > cache_size_limit:
                    self.CLI['back_cache']=self.CLI['back_cache'][:-1]
            if len(self.CLI['forward_cache']) > cache_size_limit:
                while len(self.CLI['forward_cache']) > cache_size_limit:
                    self.CLI['forward_cache']=self.CLI['forward_cache'][:-1]
        def __wrap_output_str_to_CLI_window(self,print_str,**kwargs):
            output_str_list=wrap(print_str,width=self.width_limit,replace_whitespace=False,tabsize=floor(self.width_limit/self.current_settings['TabSizeDivisor']),fix_sentence_endings=self.current_settings['FixSentenceEndings'])
            fmt_str_output=''
            for str_iter in output_str_list:
                fmt_str_output+=str_iter+'\n'
            fmt_str_output = fmt_str_output.replace('\n ','\n') # LINE TRANSITION EXCEPTION HANDLING 2: removing unnecessary spacing at the beginning of lines due to punctuation
            return fmt_str_output
        def __obtain_params_dict_for_cmd(self,cmd_name):
            output_params_dict={}
            cmd_classification=self.__obtain_command_classification(cmd_name)
            cmd_metadata_dict=self.cmd_metadata[('{}_commands'.format(cmd_classification))][cmd_name]
            for prm_iter in cmd_metadata_dict['allowed_params_list']:
                output_params_dict[prm_iter]=self.cmd_metadata['command_parameters'][prm_iter]
            return output_params_dict
        def __parse_user_cmd_parameters_str(self,operation_control_dict):
            cmd_not_accepted_error_message="Error! Input command not accepted."
            currently_iterating_new_param=True
            str_with_spaces_reading_mode=False
            current_spaced_input_string=''
            for cmds_iter in split_input_str_components[1:]:
                if (currently_iterating_new_param and (cmds_iter in self.cwd_metadata['command_parameters_syntax_list']) and (not str_with_spaces_reading_mode)):




                    currently_iterating_new_param=False if currently_iterating_new_param else True


                else:
                    if str_with_spaces_reading_mode: # case that this iteration of the loop is in the middle of reading through entries as pieces of a much larger string that has been broken apart by the splitting process and must be reassmbled with context about where quotation marks are placed in the user's parameter inputs (these specify parameter values)
                        current_spaced_input_string+=' ' +

                    string_with_spaces_exception_handling=False
                    if (cmds_iter[0] == '"') or (cmds_iter[0] == "'") or (cmds_iter[0:2] == '"""'): # case that a string containing spaces is the param argument. starting with this iteration of the loop

                        str_with_spaces_reading_mode=True

                    elif (cmds_iter.endswith('"""') or cmds_iter.endswith('"') or cmds_iter.endswith("'")) and str_with_spaces_reading_mode: # case that this iteration of the loop is the final segment of the current spaced string we're trying to parse through



                    #
                    else:

                        currently_iterating_new_param=False if currently_iterating_new_param else True
        def __extract_params_from_input_cmd_str(self, operation_control_dict):
            cmd_not_accepted_error_message="Error! Input command not accepted."
            params_are_valid=False
            params_syntax_list,params_names_list=[],[]
            valid_params_condition_1=True if ((len(split_input_str_components[1:])% 2) == 0) else False # valid params check 1: an even number of elements in list (minus command itself--implies that params and param values are 1:1)
            if valid_params_condition_1: # fill out params_syntax_list, params_names_list and output_params_dict
                params_dict=self.__parse_user_cmd_parameters_str(operation_control_dict)
            else:
                print((cmd_not_accepted_error_message + ' This happened because one or more of the terms denoting values for command parameters could not be recognized--please try again!. Make sure that any strings with spaces in them are denoted with any of the following when inputted =====> [{}, "<str>", """<str>"""]'.format("'<str>'")))
                return {}

            valid_params_condition_2=True if (() and ()) else False # valid params condition 2: specified params themselves are 1. valid for DTK_CLI as a whole and 2. valid for the specific function being called.

            if (cmd_is_valid and valid_params_condition_1 and valid_params_condition_2): # fill in output dict
                return_blank_outputs=False
        def __user_input_cmd_compiler(self, str_to_format, cmd_not_accepted_error_message="Error! Input command not accepted."):
            cmd_not_accepted_error_message="Error! Input command not accepted."
            self.CLI['viable_cmds']=self.__get_all_valid_commands_for_current_windows() # check local directory, manual access and CLI mode metadata to determine this on-the-spot
            split_input_str_components=str_to_format.split(' ')
            output_params_dict={'original_input':str_to_format,'split_input_list':split_input_str_components}
            # VALID CMD CHECK
            cmd_is_valid = False # valid cmd check
            if split_input_str_components[0] in [vci for vci in self.CLI['viable_cmds']]:
                cmd_is_valid = True
                output_user_input_dict['cmd_syntax']=split_input_str_components[0]
                for
                output_user_input_dict['cmd_syntax']=split_input_str_components[0]
            if cmd_is_valid:

            else:
                print(cmd_not_accepted_error_message + ' This happened because the term denoting the command itself could not be recognized. Please try again.')
                return {}










            original_str=str_to_format
            self.CLI['viable_cmds']=self.__get_all_valid_commands_for_current_windows()
            valid_command_name_list=[cmdi for cmdi in self.CLI_viable_cmds]
            valid_command_syntax_list=[self.CLI_viable_cmds[stx]['CLI_syntax'].lower() for stx in self.CLI_viable_cmds]
            first_double_dashes_encountered=False
            cmd_input_contains_params=True if ('--' in str_to_format) else False
            cmd_is_valid_check=True
            cmd_params_are_valid_check=True
            print_error_message=False
            output_dict={}
            cmd_str,cmd_name='',''
            if cmd_input_contains_params: # case for param parsing
                # identify core command
                cmd_is_valid_check=True0
                while str_to_format[0:1] != '--':
                    cmd_str+=str_to_format[0]
                    str_to_format=str_to_format[1:]
                # check to make sure specified command == valid
                if cmd_str == '':
                    cmd_is_valid_check=False
                else:
                    for cmdni in self.CLI_viable_cmds:
                        if self.CLI_viable_cmds[cmdni]['CLI_syntax'].replace(' ', '') == cmd_str.replace(' ',''):
                            cmd_name=cmdni
                    cmd_is_valid_check=True if (cmd_name in [cmdn for cmdn in self.CLI_viable_cmds]) else False
                str_to_format=str_to_format.replace((cmd_str + ' '),'').replace(cmd_str,'')
                # fill param dict
                parameter_dict={}
                for parami in self.cmd_metadata['command_parameters']:
                    if parami['CLI_syntax'] in str_to_format:
                        temp_param_subdict=self.cmd_metadata['command_parameters'][parami]
                        temp_param_subdict['input_arg']=''
                        parameter_dict[parami]=temp_param_subdict
                # check to make sure params are allowed with the core command
                cmd_params_are_valid_check=True
                for paramni in parameter_dict:
                    if param_dict[paramni]['CLI_syntax'] not in self.CLI_viable_cmds[cmd_name]['CLI_syntax']:
                        cmd_params_are_valid_check=False
                print_error_message=False if (cmd_is_valid_check and cmd_params_are_valid_check) else True
                # identify param values
                split_inputs_list=str_to_format.split(' ')
                current_element_is_param_syntax=True
                current_param_syntax=''
                current_param_value=''
                while len(split_inputs_list) > len([]):
                    if current_element_is_param_syntax:
                        current_param_syntax=split_inputs_list[0]
                        current_element_is_param_syntax=False
                    else:
                        current_param_value=split_inputs_list[0]
                        for paramni in parameter_dict:
                            if parameter_dict[paramni]['CLI_syntax'] == current_param_syntax:
                                parameter_dict[paramni]['input_arg']=current_param_value
                        current_element_is_param_syntax=True
                        current_param_syntax=''
                        current_param_value=''
                    split_inputs_list=split_inputs_list[1:]
            else: # case for just cmd identification with no params
                str_to_format=str_to_format.replace(' ','').replace('\n','').lower()
                print_error_message=False if str_to_format in valid_command_syntax_list else False
                parameter_dict=''
                if not print_error_message:
                    for cmdni in valid_command_name_list:
                        if self.CLI_viable_cmds[cmdni]['CLI_syntax'] == str_to_format:
                            cmd_name=cmdni
                            cmd_str=self.CLI_viable_cmds[cmdni]['CLI_syntax']
            if print_error_message:
                cmd_not_accepted_error_message="""
                Error! Input command not accepted. Please try again.
                """
                print(cmd_not_accepted_error_message)
                self.__update_txt_session_log(cmd_not_accepted_error_message)
            else:
                output_dict={'original_str':original_str,
                                 'cmd_name':cmd_name,
                                 'cmd_str':cmd_str,
                                 'parameters':parameter_dict}
                return output_dict
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
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
            self.bookmarks=self.__load_bookmarks()
            self.usage_data=self.__load_usage_data()
            self.cmd_metadata=self.__load_cmd_metadata()
            self.default_settings=self.__load_default_settings()
            self.current_settings=self.__load_current_settings()
            self.dividers=self.__load_dividers()
            self.first_input_exception=True
            self.CLI={
                      'cwd':(self.current_settings['HomePathString']) if (jump_to_path == None) else jump_to_path,
                      'mode':self.start_mode,
                      'back_cache':[], # !!! NOTE: 0 INDEX IS MOST RECENT FOR NAVIGATION CACHES !!!
                      'forward_cache':[], # !!! NOTE: 0 INDEX IS MOST RECENT FOR NAVIGATION CACHES !!!
                      'manual_override_mode':self.manual_override_mode,
                      'exec_str':'',
                      'viable_cmds':['__ToggleHomePage'],
                     }
            self.session_log={'timestamps':[self.__obtain_fmt_datetime_as_str(), None],'saved_str_blocks':[]}
    #####################################################
    ## DEVELOPER_TOOLKIT_COMMAND_LINE_INTERFACE CLASS ###
    #####################################################
    class DTK_CLI(MethodHelper__DTK_CLI):
        def __init__(self,**kwargs):
            super().__init__(**kwargs)
        ##########################
        ### PAGE DISPLAY LOGIC ###
        ##########################
        def __StatusBar_display(self):
            output_text_str="{}\n\nHELP--> [?] EXIT--> [X] PATH OPEN--> [O --p] [<] BACK|FORWARD [>] HOME--> [H] SETTINGS--> [S --t --v] BOOKMARKS--> [B --<o or s> --i]\n".format(self.dividers['Divider_XXL']['proportioned'],('EXEC--> [E]' if self.manual_override_mode else ''),self.CLI['cwd'],self.dividers['Divider_XXL']['proportioned'])
            return output_text_str
        def __HomePage_display(self):
            output_text_str="{}\n\n\n{}\n{}>>>>>>  DEVELOPER TOOLKIT COMMAND LINE INTERFACE  ||  VER. {}\n{}>>>  CREATED BY {}, DATED {}\n{}\n\n\n{}".format(self.dividers['Divider_XXL']['proportioned'],self.dividers['Divider_XXL']['proportioned'],self.dividers['Divider_XS']['proportioned'],self.about['Version'],self.dividers['Divider_XXS']['proportioned'],self.about['Author'],self.about['Created'],self.dividers['Divider_XXL']['proportioned'],self.dividers['Divider_XXL']['proportioned'])
            return self.__wrap_output_str_to_CLI_window(output_text_str)
        def __HelpMenu_display(self):
            top_help_str_to_display="""
            {} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} GENERAL HELP (PRESS ANY KEY TO EXIT)\n{}
            """.format(self.dividers['Divider_XXL']['proportioned'], self.dividers['Divider_XXL']['proportioned'],self.dividers['Divider_S']['proportioned'],self.dividers['Divider_XXL']['proportioned'])
            global_commands_help_text=self.dividers['Divider_XS']['proportioned']+'GLOBAL COMMANDS:\n'
            global_commands=self.cmd_metadata['global_commands']
            path_specific_commands=self.cmd_metadata['path_specific_commands']
            global_commands_names=[cmdn for cmdn in global_commands]
            path_specific_commands_names=[cmdn for cmdn in path_specific_commands]
            if self.CLI['manual_override_mode']:
                manual_commands=self.cmd_metadata['manual_commands']
                manual_commands_names=[cmdn for cmdn in manual_commands]
            else:
                manual_commands={}
                manual_commands_names=[]
            total_commands_names=global_commands_names + path_specific_commands_names + manual_commands_names
            for gcmd in total_commands_names:
                text_temp=self.dividers['Divider_XXS']['proportioned']+'[{}]: {}\n--> Called by using any of: '.format(gcmd, global_commands[gcmd]['description'])
                possible_calls_list,possible_calls_str=global_commands[gcmd]['allowed_variations'],''
                for pcalls in possible_calls_list:
                    possible_calls_str+=pcalls
                text_temp+=possible_calls_str
                global_commands_help_text+=text_temp
            output_text_str=top_help_str_to_display + global_commands_help_text
            return self.__wrap_output_str_to_CLI_window(output_text_str)
        def __SettingsMenu_display(self):
            top_display="{}\n{}>>>>>> SETTINGS\n{} (INPUT TO EXIT BACK TO home--> S)".format(self.dividers['Divider_XXL']['proportioned'], self.dividers['Divider_XS']['proportioned'], self.dividers['Divider_XXL']['proportioned'], self.dividers['Divider_XXL']['proportioned'])
            default_settings_str,current_settings_str='',
            for dsi in self.default_settings:
                iname,ivalue=dsi,self.default_settings[dsi]
                default_settings_str+=self.dividers['Divider_XXS']['proportioned']+ iname + ': ' + value + '\n'
            for csi in self.current_settings:
                iname,ivalue=dsi,self.current_settings[csi]
                current_settings_str+=self.dividers['Divider_XXS']['proportioned']+ iname + ': ' + value + '\n'
            output_text_str=top_display + "DEFAULT SETTINGS:\n{}\nCURRENT SETTINGS:\n{}".format(default_settings_str,current_settings_str)
            return_str=self.__wrap_output_str_to_CLI_window(output_text_str)
            return return_str
        def __BookmarksBar_display(self):
            output_text_str="{}\n{}>>>>>> BOOKMARKS\n{}\n".format(self.dividers['Divider_XXL']['proportioned'], self.dividers['Divider_XS']['proportioned'],self.dividers['Divider_XXL']['proportioned'])
            for bki in self.bookmarks:
                output_text_str+=self.dividers['Divider_XXS']['proportioned']+"{} | {}\n".format(bki,self.bookmarks[bki]['name'])
            return self.__wrap_output_str_to_CLI_window(print_str=output_text_str)
        def __PrintContents_display(self):
            top_str="\n{}\n{}>>>>>> CONTENTS DISPLAYED FOR PATH: <{}>\n{}\n".format(self.dividers['Divider_XXL']['proportioned'], self.dividers['Divider_XS']['proportioned'],self.dividers['Divider_XXL']['proportioned'], self.CLI['cwd'],self.dividers['Divider_XXL']['proportioned'])
            cwd_contents=Path(self.CLI['cwd']).read_text().split('\n')
            cwd_contents_str=''
            for conti in cwd_contents:
                cwd_contents_str+=conti + '\n'
            return self.__wrap_output_str_to_CLI_window(print_str=top_str + cwd_contents_str)
        def __PrintPreview_display(self):
            top_str="\n{}\n{}>>>>>> PREVIEW DISPLAY PATH: <{}>\n{}\n".format(self.dividers['Divider_XXL']['proportioned'], self.dividers['Divider_XS']['proportioned'],self.dividers['Divider_XXL']['proportioned'], self.CLI['cwd'],self.dividers['Divider_XXL']['proportioned'])
            if os.path.isfile(self.CLI['cwd']):
                cwd_contents=Path(self.CLI['cwd']).read_text().split('\n')[0:self.current_settings['HeightLimit']]
            else:
                cwd_contents=['{}>>> SUB-DIRECTORIES:\n'.format(self.dividers['Divider_XXS']['proportioned'])]
                subdirs_list, files_list=[],[]
                for diri in os.listdir():
                    diri_str=self.dividers['Divider_XXS']['proportioned']+'>>' + diri + ' | PATH: ' + os.path.abspath(diri) +'\n'
                    if os.path.isfile(diri):
                        files_list.append(diri_str)
                    else:
                        subdirs_list.append(diri_str)
                for sdli in subdirs_list:
                    cwd_contents.append(sdli)
                cwd_contents.append('{}>>> FILES IN FOLDER:\n'.format(self.dividers['Divider_XXS']['proportioned']))
                for flli in files_list:
                    cwd_contents.append((self.dividers['Divider_XXS']['proportioned'] + '>> ' + flli + ' | PATH: ' + os.path.abspath(diri)+ '\n'))
            cwd_contents_str=''
            for conti in cwd_contents:
                cwd_contents_str+=conti
            return self.__wrap_output_str_to_CLI_window(top_str + cwd_contents_str)
        def __execStringInput_display(self):
            if self.CLI['manual_override_mode'] and (self.CLI['mode'] == 'exec_str'):
                exec_display_str="\n{}\n{}>>>>>> DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} MANUAL OVERRIDE MODE exec() CALL\n{}\nRUNNING CODE: \nexec(\n".format(self.dividers['Divider_XXL']['proportioned'],self.dividers['Divider_XS']['proportioned'],self.dividers['Divider_XXL']['proportioned'],self.dividers['Divider_XXL']['proportioned'])
                exec_display_str+=self.CLI['exec_str'] + '\n     )\n{}\n'.format(self.dividers['Divider_XXL']['proportioned'])
                return self.__wrap_output_str_to_CLI_window(exec_display_str)
            else:
                no_MO_error_str='Error! Function DTK_CLI.__execStringInput_display() cannot activate without DTK_CLI.CLI["manual_override_mode"] being True.'
                return self.__wrap_output_str_to_CLI_window(no_MO_error_str)
        ################################
        ### NAVIGATION COMMAND LOGIC ###
        ################################
        def __TeleportToSpecifiedPath(self,to_path,print_preview_not_contents=True):
            self.CLI['back_cache']=[self.CLI['cwd'],self.CLI['mode']] + self.CLI['back_cache'][:-1]
            self.CLI['forward_cache']=[]
            self.CLI['cwd']=to_path
            self.__update_usage_data(self.CLI['cwd'])
            self.CLI['mode']='PrintPreview' if print_preview_not_contents else 'PrintContents'
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def __NavigateBack(self):
            if len(self.CLI['forward_cache'])==len([]):
                nowhere_to_navigate_back_error_str="ERROR! The interface has not stored any valid directories for the back button to navigate to as of yet."
                print(nowhere_to_navigate_forward_error_str)
            else:
                to_path=self.CLI['back_cache'][0][0]
                to_mode=self.CLI['back_cache'][0][1]
                self.CLI['back_cache']=self.CLI['back_cache'][1:]
                self.CLI['forward_cache']=[[self.CLI['cwd'],self.CLI['mode']]] + self.CLI['forward_cache'][:-1]
                self.CLI['cwd']=to_path
                self.CLI['mode']=to_mode
                self.__update_usage_data(self.CLI['cwd'])
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def __NavigateForward(self):
            if len(self.CLI['forward_cache'])==len([]):
                nowhere_to_navigate_forward_error_str="ERROR! The interface has not stored any valid directories for the forward button to navigate to as of yet."
                print(nowhere_to_navigate_forward_error_str)
            else:
                to_path=self.CLI['forward_cache'][0][0]
                to_mode=self.CLI['forward_cache'][0][1]
                self.CLI['back_cache']=self.CLI['forward_cache'][0] + self.CLI['back_cache']
                self.CLI['forward_cache']=self.CLI['forward_cache'][1:]
                self.CLI['cwd']=to_path
                self.CLI['mode']=to_mode
                if to_mode == 'PrintPreview' or to_mode == 'PrintContents':
                    self.__update_usage_data(self.CLI['cwd'])
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def __ParentDirectory(self):
            parent_path=Path(self.CLI['cwd']).parent.absolute()
            self.CLI['back_cache']=[[self.CLI['cwd'], self.CLI['mode']]] + self.CLI['back_cache'][:-1]
            self.CLI['forward_cache']=[]
            self.CLI['cwd']=parent_path
            self.CLI['mode']='PrintPreview'
            self.__update_usage_data(self.CLI['cwd'])
            self.__trim_navigate_forwards_or_backwards_path_history_lists()
        def __PrintPreview(self,to_path):
            self.__TeleportToSpecifiedPath(to_path)
        def __PrintContents(self,to_path):
            if os.path.isfile(self.CLI['cwd']):
                self.__TeleportToSpecifiedPath(to_path, print_preview_not_contents=False)
            else:
                no_printable_contents_error_str="Error! The current CLI windows path == not available for viewing, only previewing. Likely this == due to the windows path being set to a folder and not a file."
                print(no_printable_contents_error_str)
        ##############################
        ### COMMAND-SPECIFIC LOGIC ###
        ##############################
        def __ToggleHomePage(self):
            self.CLI['back_cache']=[[self.CLI['cwd'],self.CLI['mode']]]+self.CLI['back_cache'][1:]
            self.CLI['forward_cache']=[]
            self.CLI['mode']='home'
            self.CLI['cwd']=self.src_dir_path
            self.__update_usage_data(self.CLI['cwd'])
        def __ToggleHelpMenuDisplay(self):
            self.CLI['back_cache']=[[self.CLI['cwd'],self.CLI['mode']]]+self.CLI['back_cache'][1:]
            self.CLI['forward_cache']=[]
            self.CLI['mode']='Help' if self.CLI['mode']!='Help' else 'PrintPreview'
        def __ToggleSettingsDisplay(self):
            self.CLI['back_cache']=[[self.CLI['cwd'],self.CLI['mode']]]+self.CLI['back_cache'][1:]
            self.CLI['forward_cache']=[]
            self.CLI['mode']='Settings' if self.CLI['mode']!='Settings' else 'PrintPreview'
        def __ResetSettingsToDefaults(self):
            self.current_settings=self.default_settings
        def __ToggleSettingsValue(self, setting_name, change_value_to_this):
            self.current_settings[setting_name]=change_value_to_this
            if self.current_settings['RESET_TO_DEFAULT']:
                self.__ResetSettingsToDefaults()
        def __OpenBookmarksBar(self):
            self.CLI['mode']='Bookmarks'
        def __SaveCurrentPathAsBookmark(self):
            print("Please input name for the new bookmark of path: {}".format(self.CLI['cwd']))
            bookmark_name=input()
            if self.CLI['cwd'] in [k for k in self.usage_count]:
                usage_ct=self.usage_count[self.CLI['cwd']]
            else:
                usage_ct=0
            self.bookmarks[self.CLI['cwd']]={'name':bookmark_name,'bookmark_usage_count':usage_ct}
        def __OpenBookmark(self,name_or_path):
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
        def __execStringInput(self, exec_file_path_or_str):
            if os.path.exists(exec_file_path_or_str) and exec_file_path_or_str.endswith('.txt'):
                with open(exec_file_path_or_str, 'r') as opentxt:
                    exec_str=opentxt.read()
            else:
                exec_str=exec_file_path_or_str
            self.CLI['exec_str']=exec_str
            self.CLI['mode']='exec_str'
        def __ExitCLI(self):
            self.session_log['timestamps'][1]=self.__obtain_fmt_datetime_as_str()
            self.session_log_path=self.src_dir_path  + 'session_from_{}_to_{}.txt'.format(self.session_log['timestamps'][0],self.session_log['timestamps'][1])
            self.__update_usage_data_for_bookmarks_dicts()
            self.__save_new_metadata_to_files()
            self.__save_session_log_as_txt()
            self.POWER=False
        ######################
        ### CLI LOOP LOGIC ###
        ######################
        def __CLI_display(self):
            def __top_header(): # TOP
                if self.current_settings['StatusBarPosition']=='top':
                    status_bar_str=self.__StatusBar_display()
                    self.__update_txt_session_log(status_bar_str)
                    print(status_bar_str)
                else:
                    divider_line_1=self.dividers['Divider_XXL']['proportioned'] + '\n\n' + self.dividers['Divider_M']['proportioned'] + '<<<  dtk-cli.py  >>>' + self.dividers['Divider_M']['proportioned']
                    if self.current_settings['PrintInterfaceMetadata']:
                        divider_line_2="\n{}|||| CURRENT: {} || {} || {} ||||{}\n".format(self.dividers['Divider_XXS']['proportioned'],self.__obtain_fmt_datetime_as_str(),self.CLI['cwd'], self.CLI['mode'],self.dividers['Divider_XXS']['proportioned'])
                        divider_line_2=self.__wrap_output_str_to_CLI_window(divider_line_2)
                    else:
                        divider_line_2=''
                print(divider_line_1)
                print(divider_line_2)
                self.__update_txt_session_log(divider_line_1)
                self.__update_txt_session_log(divider_line_2)
            def __midsection(): # MID
                if self.CLI['mode'] == 'home':
                    save_and_print_me=self.__HomePage_display()
                elif self.CLI['mode'] == 'help':
                    save_and_print_me=self.__HelpMenu_display()
                elif self.CLI['mode'] == 'settings':
                    save_and_print_me=self.__SettingsMenu_display()
                elif self.CLI['mode'] == 'bookmarks':
                    save_and_print_me=self.__BookmarksBar_display()
                elif self.CLI['mode'] == 'execFileContents':
                    save_and_print_me=self.__execStringInput_display()
                elif os.path.exists(self.CLI['cwd']):
                    if self.CLI['mode']=='PrintPreview':
                        self.__PrintPreview_display()
                    elif self.CLI['mode']=='PrintContents' and (not os.path.isfile(self.CLI['cwd'])):
                        self.__PrintContents_display()
                else:
                    save_and_print_me="ERROR! DTK_CLI.CLI_cwd does not point to a valid page for the command line interface to display. In the worst case, please restart the program."
                self.__update_txt_session_log(save_and_print_me)
                print(save_and_print_me)
            def __bottom_header(): # LOW
                if self.current_settings['StatusBarPosition']=='bottom':
                    status_bar_str=self.__StatusBar_display()
                    self.__update_txt_session_log(status_bar_str)
                    print(status_bar_str)
                else:
                    divider_line=self.dividers['Divider_L']['proportioned'] + '\n' + self.dividers['Divider_M']['proportioned'] + 'DTK-CLI' + self.dividers['Divider_M']['proportioned'] + '\n'+ self.dividers['Divider_L']['proportioned']
                    self.__update_txt_session_log(divider_line)
                    print(divider_line)
            def __misc_display_logic(): # MISC
                if self.CLI['mode'] == 'execFileContents':
                    print_exec_str=self.CLI['exec_str']
                    self.CLI['exec_str']=''
                    exec(print_exec_str)
            __top_header()
            __midsection()
            __bottom_header()
            __misc_display_logic()
        def __CLI_cmd(self,input_cmd_str):
            self.user_input_dict=self.__user_input_cmd_compiler(input_cmd_str)
            if self.user_input_dict['parameters'] != {}:
                fn_inputs=''
                for paramsi in [prmi for prmi in self.user_input_dict['parameters']]:
                    fn_inputs+=paramsi + '=' + self.user_input_dict['parameters'][paramsi]['input_arg'] + ','
            else:
                fn_inputs=''
            while fn_inputs.endswith(','):
                fn_inputs=fn_inputs[:-1]
            input_cmd_name=self.user_input_dict['cmd_name']
            if input_cmd_name!='':
                self.__ToggleHomePage()
            else:
                cmd_fn_name=self.cmd_metadata[self.user_input_dict['cmd_name']]['cmd_fn_name']
        def __CLI(self):
            while self.POWER:
                os.chdir(self.CLI['cwd'])
                self.__CLI_display()
                if self.first_input_exception:
                    CLI_input='H'
                    self.first_input_exception=False
                else:
                    CLI_input=input()
                self.__CLI_cmd(CLI_input)
    ##########################################################
    ## DTK_CLI CLASS INSTANCE AND CALLING INTERFACE METHOD ###
    ##########################################################
    dtk_cli_obj_instance=DTK_CLI()
    dtk_cli_obj_instance.__CLI()
################################################################
### main() FUNCTION CALLED VIA OPENING FILE THROUGH TERMINAL ###
################################################################
if __name__=='__main__':
    main()
