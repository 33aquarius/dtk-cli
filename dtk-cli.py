#####################################################################
### dtk-cli.py -- DEVELOPER TOOLKIT COMMAND LINE INTERFACE OBJECT ###
#####################################################################
__author__="Eamon Smith (github.com/34m0n-dev)"
__version__='1'
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

    #####################################################
    ## DEVELOPER_TOOLKIT_COMMAND_LINE_INTERFACE CLASS ###
    #####################################################
    class DTK_CLI:

        ######################
        ### CLI OPERATIONS ###
        ######################
        def __obtain_fmt_datetime_as_str(self,unix_time_or_now='now'):
            return_datetime_str=''
            if 'current_settings' in dir(self):
                strftime_fmt = self.current_settings['StatusBarDateTimeFormat']
            else:
                strftime_fmt = '%Y-%m-%d %H:%M:%S'
            if unix_time_or_now=='now':
                return_datetime_str=datetime.utcfromtimestamp(time.time()).strftime(strftime_fmt)
            elif (isinstance(unix_time_or_now), int) or (isinstance(unix_time_or_now, float)):
                return_datetime_str=datetime.utcfromtimestamp(unix_time_or_now).strftime(strftime_fmt)
            else:
                bad_ftm_for_time_input_error_str="""
                ERROR! DATETIME CANNOT BE DISPLAYED PROPERLY. PLEASE REFERENCE DTK_CLI.__obtain_fmt_datetime_as_str() FOR DETAILS.
                """
                print(bad_ftm_for_time_input_error_str)
                return_datetime_str='DATETIME ERROR'
            return return_datetime_str
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
        def __get_all_valid_commands_for_current_windows(self):
            output_valid_commands_dict=(self.cmd_metadata['manual_commands']) if self.CLI['manual_override_mode'] else {}
            for cmdi in self.cmd_metadata['global_commands']:
                output_valid_commands_dict[cmdi]=self.cmd_metadata['global_commands'][cmdi]
            for cmdi in self.cmd_metadata['path_commands']:
                if cmdi in ['TeleportToSpecifiedPath', 'NavigateForward', 'NavigateBack','ParentDirectory','SaveCurrentPathAsBookmark']:
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_commands'][cmdi]
                elif cmdi=='PrintPreview' and (self.CLI['mode']=='PrintContents'):
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_commands'][cmdi]
                elif cmdi=='PrintContents' and self.CLI['mode']=='PrintPreview':
                    output_valid_commands_dict[cmdi]=self.cmd_metadata['path_commands'][cmdi]
            self.CLI_viable_cmds=output_valid_commands_dict
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
        def __wrap_output_str_to_CLI_window(self,print_str):
            output_str_list=wrap(print_str,width=self.width_limit,tabsize=floor(self.width_limit/self.current_settings['TabSizeDivisor']),fix_sentence_endings=self.current_settings['FixSentenceEndings'])
            fmt_str_output=''
            for str_iter in output_str_list:
                fmt_str_output+=str_iter+'\n'
            fmt_str_output = fmt_str_output.replace('\n ','\n') # LINE TRANSITION EXCEPTION HANDLING 2: removing unnecessary spacing at the beginning of lines due to punctuation
            return fmt_str_output

        def __user_input_cmd_compiler(self, str_to_format):
            original_str=str_to_format
            self.__get_all_valid_commands_for_current_windows()
            valid_command_name_list=[cmdi for cmdi in self.CLI_viable_cmds]
            valid_command_syntax_list=[stx['CLI_syntax'].lower() for stx in valid_command_name_list]
            first_double_dashes_encountered=False
            cmd_input_contains_params=True if ('--' in str_to_format) else False
            cmd_name=''
            cmd_is_valid_check=True
            cmd_params_are_valid_check=True
            print_error_message=False
            if cmd_input_contains_params: # case for param parsing
                # identify core command
                cmd_str=''
                cmd_name=''
                cmd_is_valid_check=True
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
                cmd_name=''
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
                output_cmd_dict={'original_str':original_str,
                                 'cmd_name':cmd_name,
                                 'cmd_str':cmd_str,
                                 'parameters':parameter_dict}
                return output_dict

        ###################################
        ### CLI TEXT OUTPUT & CMD LOGIC ###
        ###################################
        def __status_bar_display(self):
            output_text_str="{}\n\nHELP--> [?] EXIT--> [X] PATH OPEN--> [O --p] [<] BACK|FORWARD [>] \nHOME--> [H] SETTINGS--> [S --t --v] BOOKMARKS--> [B --<o or s> --i]\n\n".format(self.dividers['DividerLarge']['proportioned'],('EXEC--> [E]' if self.manual_override_mode else ''),self.CLI['cwd'],self.dividers['DividerLarge']['proportioned'])
            return output_text_str
        def __HomePage_display(self):
            output_text_str="{}\n\n\n{}\nDEVELOPER TOOLKIT COMMAND LINE INTERFACE VER. {}\n                    ----------\nCREATED BY {}ON {}\n{}\n\n\n{}\n{}".format(self.dividers['DividerLarge']['proportioned'],self.dividers['DividerLarge']['proportioned'],self.about['Version'],self.about['Author'],self.about['Created'],self.dividers['DividerLarge']['proportioned'],self.dividers['DividerLarge']['proportioned'],self.dividers['DividerLarge']['proportioned'])
            return output_text_str
        def __HelpMenu_display(self):
            top_help_str_to_display="""
            {} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} HELP SCREEN (PRESS ANY KEY TO EXIT)\n{}
            """.format(self.dividers['DividerLarge']['proportioned'], self.dividers['DividerMedium']['proportioned'],self.dividers['DividerSmall']['proportioned'])
            global_commands_help_text='GLOBAL COMMANDS:\n---------------\n'
            global_commands=self.cmd_metadata['global_commands']
            path_commands=self.cmd_metadata['path_commands']
            global_commands_names=[cmdn for cmdn in global_commands]
            path_commands_names=[cmdn for cmdn in path_commands]
            if self.CLI['manual_override_mode']:
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
            return self.__wrap_output_str_to_CLI_window(print_str=output_text_str)
        def __SettingsMenu_display(self):
            top_display="\n{} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} SETTINGS\n{}(INPUT TO EXIT BACK TO home--> S)".format((self.current_settings['DividerLarge'] * ceil((self.current_settings['WidthLimit'] / 3))), (self.current_settings['DividerMedium'] * ceil((self.current_settings['WidthLimit'] / 5))), (self.current_settings['DividerSmall'] * ceil((self.current_settings['WidthLimit'] / 7))))
            default_settings_str,current_settings_str='',''
            for dsi in self.default_settings:
                iname,ivalue=dsi,self.default_settings[dsi]
                default_settings_str+='  ->' + iname + ': ' + value + '\n'
            for csi in self.current_settings:
                iname,ivalue=dsi,self.current_settings[csi]
                current_settings_str+='  ->' + iname + ': ' + value + '\n'
            output_text_str=top_display + "DEFAULT SETTINGS:\n{}\nCURRENT SETTINGS:\n{}".format(default_settings_str,current_settings_str)
            return_str=self.__wrap_output_str_to_CLI_window(output_text_str)
            return return_str
        def __BookmarksBar_display(self):
            output_text_str="\n{} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{}\nBOOKMARKS\n{}\n".format(self.dividers['DividerLarge']['proportioned'], self.dividers['DividerMedium']['proportioned'],self.dividers['DividerSmall']['proportioned'])
            for bki in self.bookmarks:
                output_text_str+="  ->{} | {}\n".format(bki,self.bookmarks[bki]['name'])
            return self.__wrap_output_str_to_CLI_window(print_str=output_text_str)
        def __PrintContents_display(self):
            top_str="\n{}\nDEVELOPER TOOLKIT:\n{}\nCONTENTS DISPLAY FOR FILE OR FOLDER\n{}\n".format(self.dividers['DividerLarge']['proportioned'],self.dividers['DividerMedium']['proportioned'],self.dividers['DividerSmall']['proportioned'])
            cwd_contents="CONTENTS:\n" + Path(self.CLI['cwd']).read_text().split('\n')
            cwd_contents_str=''
            for conti in cwd_contents:
                cwd_contents_str+=conti + '\n'
            return self.__wrap_output_str_to_CLI_window(print_str=top_str + cwd_contents_str)
        def __PrintPreview_display(self):
            top_str="\n{}\nDEVELOPER TOOLKIT:\n{}\nPREVIEW DISPLAY FOR FILE OR FOLDER\n{}\n".format(self.dividers['DividerLarge']['proportioned'],self.dividers['DividerMedium']['proportioned'],self.dividers['DividerSmall']['proportioned'])
            if os.path.isfile(self.CLI['cwd']):
                cwd_contents=Path(self.CLI['cwd']).read_text().split('\n')[0:self.current_settings['HeightLimit']]
            else:
                cwd_contents=['\nSUB-DIRECTORIES:\n']
                subdirs_list, files_list=[],[]
                for diri in os.listdir():
                    diri_str='  ->' + diri + ' | PATH: ' + os.path.abspath(diri) +'\n'
                    if os.path.isfile(diri):
                        files_list.append(diri_str)
                    else:
                        subdirs_list.append(diri_str)
                for sdli in subdirs_list:
                    cwd_contents.append(sdli)
                cwd_contents.append('\nFILES IN FOLDER:\n')
                for flli in files_list:
                    cwd_contents.append(flli)
            cwd_contents_str=''
            for conti in cwd_contents:
                cwd_contents_str+=conti + '\n'
            return self.__wrap_output_str_to_CLI_window(top_str + cwd_contents_str)
        def __execStringInput_display(self):
            if self.CLI['manual_override_mode'] and (self.CLI['mode'] == 'exec_str'):
                exec_display_str="\n{} DEVELOPER TOOLKIT COMMAND LINE INTERFACE\n{} MANUAL OVERRIDE MODE exec() CALL\n{}\nNOW RUNNING: \n exec(\n".format(self.dividers['DividerLarge']['proportioned'],self.dividers['DividerMedium']['proportioned'],self.dividers['DividerSmall']['proportioned'])
                exec_display_str+=self.CLI['exec_str'] + ')\n'
                return self.__wrap_output_str_to_CLI_window(exec_display_str)
            else:
                no_MO_error_str='Error! Function DTK_CLI.__execStringInput_display() cannot activate without DTK_CLI.CLI["manual_override_mode"] being True.'
                return self.__wrap_output_str_to_CLI_window(no_MO_error_str)
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
            self.CLI['back_cache']=[self.CLI['cwd'], self.CLI['mode']] + self.CLI['back_cache'][:-1]
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
        def __ReturnToHomePage(self):
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

        #####################
        ### CLI OPERATION ###
        #####################
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
        def __ExitCLI(self):
            self.session_log['timestamps'][1]=self.__obtain_fmt_datetime_as_str()
            self.session_log_path=self.src_dir_path  + 'session_from_{}_to_{}.txt'.format(self.session_log['timestamps'][0],self.session_log['timestamps'][1])
            self.__update_usage_data_for_bookmarks_dicts()
            self.__save_new_metadata_to_files()
            self.__save_session_log_as_txt()
            self.POWER=False
        def __CLI_display(self):
            # TOP
            if self.current_settings['StatusBarPosition']=='top':
                status_bar_str=self.__status_bar_display()
                self.__update_txt_session_log(status_bar_str)
                print(status_bar_str)
            else:
                divider_line=self.dividers['DividerLarge']['proportioned'] + '\n' + self.dividers['DividerMedium']['proportioned'] + 'DTK-CLI' + self.dividers['DividerMedium']['proportioned'] + '\n'+ self.dividers['DividerLarge']['proportioned']
                self.__update_txt_session_log(divider_line)
                print(divider_line)
            # MID
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
            # LOW
            if self.current_settings['StatusBarPosition']=='bottom':
                status_bar_str=self.__status_bar_display()
                self.__update_txt_session_log(status_bar_str)
                print(status_bar_str)
            else:
                divider_line=self.dividers['DividerLarge']['proportioned'] + '\n' + self.dividers['DividerMedium']['proportioned'] + 'DTK-CLI' + self.dividers['DividerMedium']['proportioned'] + '\n'+ self.dividers['DividerLarge']['proportioned']
                self.__update_txt_session_log(divider_line)
                print(divider_line)
            # MISC
            if self.CLI['mode'] == 'execFileContents':
                print_exec_str=self.CLI['exec_str']
                self.CLI['exec_str']=''
                exec(print_exec_str)
            if self.current_settings['PrintInterfaceMetadata']:
                interface_metadata_str="\nTIME || {}\nCWD || {}\nMODE || {}\n".format(self.__obtain_fmt_datetime_as_str(),self.CLI['cwd'], self.CLI['mode'])
                interface_metadata_str=self.__wrap_output_str_to_CLI_window(interface_metadata_str)
                self.__update_txt_session_log(interface_metadata_str)
                print(interface_metadata_str)
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
            input_cmd_name=self.user_input_dict['cwd_name']
            exec('self.__{}({})'.format(input_cmd_name, fn_inputs))

        ############
        ### INIT ###
        ############
        def __init__(
                     self,
                     src_dir_path=args.homepath,
                     jump_to_path=args.filepath,
                     jump_to_mode=args.startmode,
                     width_limit=args.width_limit,
                     height_limit=args.height_limit,
                     manual_override_pwd=args.manual_override_pwd,
                     author=author,
                     version=version,
                     created=created,
                     **kwargs
                    ):

            #####################
            ### SUB-FUNCTIONS ###
            #####################
            def __os_syntax_profiling():
                platforms={'linux1':'linux','linux2':'linux','darwin':'os_x','win32':'windows'}
                slashes={'linux':'/','windows':r'\\','os_x':'/'}
                sys_os=sys.platform if sys.platform not in platforms else platforms[sys.platform]
                sys_slashes=slashes['linux'] if sys_os not in slashes else slashes[sys_os] # assume linux syntax for slashes used in path strs
                return sys_os, sys_slashes
            def __establish_paths(src_dir_path=src_dir_path):
                src_dir_path=os.getcwd() if src_dir_path == None else src_dir_path
                sys.path.append(src_dir_path)
                return src_dir_path
            def __fetch_desktop_path():
                desktop_path=(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) # may encounter difficulties if the DTK-CLI folder == not located somewhere on desktop, thus doing so == recommended for ease of use. Otherwise, you will need to pass something else though here.
                return desktop_path
            def __load_bookmarks():
                if os.path.isfile(self.bookmarks_path):
                    with open(self.bookmarks_path, "r") as iter_json_to_load:
                        bookmarks=json.load(iter_json_to_load)
                else:
                    bookmarks={(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')):{'name':'Desktop','bookmark_usage_count':0},
                                 src_dir_path:{'name':'Toolkit home','bookmark_usage_count':0}}
                    with open(self.bookmarks_path, "w") as outfile:
                        json.dump(bookmarks, outfile)
                return bookmarks
            def __load_usage_data():
                if os.path.isfile(self.usage_data_path):
                    with open(self.usage_data_path, "r") as iter_json_to_load:
                        usage_data=json.load(iter_json_to_load)
                else:
                    usage_data={__fetch_desktop_path():0,
                                self.src_dir_path:0}
                    with open(self.usage_data_path, "w") as outfile:
                        json.dump(usage_data, outfile)
                return usage_data
            def __load_default_settings():
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
                                      'DividerLarge':'X',
                                      'DividerLarge_proportion':1,
                                      'DividerMedium':'~',
                                      'DividerMedium_proportion':2.5,
                                      'DividerSmall':'-',
                                      'DividerSmall_proportion':3.3,
                                      'ManualOverridePwd':manual_override_pwd,
                                      'StatusBarDateTimeFormat':"%H:%M:%S",
                                      'StatusBarPosition':'bottom', # 'top' or 'bottom'
                                      'PrintInterfaceMetadata':True,
                                      'RESET_TO_DEFAULT':False
                                      }
                    with open(self.default_settings_path, "w") as outfile:
                        json.dump(default_settings, outfile)
                return default_settings
            def __load_current_settings():
                current_settings={}
                if os.path.isfile(self.current_settings_path):
                    with open(self.current_settings_path, "r") as iter_json_to_load:
                        current_settings=json.load(iter_json_to_load)
                else:
                    current_settings=__load_default_settings()
                    with open(self.current_settings_path, "w") as outfile:
                        json.dump(current_settings, outfile)
                return current_settings
            def __load_dividers():
                divider_proportions={'DividerLarge':self.current_settings['DividerLarge_proportion'],
                                     'DividerMedium':self.current_settings['DividerMedium_proportion'],
                                     'DividerSmall':self.current_settings['DividerSmall_proportion']}
                proportioned_large=(self.current_settings['DividerLarge'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['DividerLarge'])))
                proportioned_medium=(self.current_settings['DividerMedium'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['DividerMedium'])))
                proportioned_small=(self.current_settings['DividerSmall'] * ceil((self.current_settings['WidthLimit'] / divider_proportions['DividerSmall'])))
                proportioned_output_dividers={'DividerLarge':{'unit':self.current_settings['DividerLarge'],
                                                                'proportioned':proportioned_large},
                                                'DividerMedium':{'unit':self.current_settings['DividerMedium'],
                                                                 'proportioned':proportioned_medium},
                                                'DividerSmall':{'unit':self.current_settings['DividerSmall'],
                                                                'proportioned':proportioned_small}}




                return proportioned_output_dividers
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
                                        'Bookmark':{'CLI_syntax':'--b',
                                                    'description':'This parameter can either be the name of a bookmark or the string of the path for the bookmark. The CLI will automatically process both.'},
                                        'execManualStr':{ 'CLI_syntax':'--exs',
                                                         'description':'This parameter can specify either the path of a .txt file which contains the string of code which will be run via exec(). The parameter can also just be the string to be passed through exec() as well--the CLI will attempt to distinguish this by checking if the string == a valid path.'}
                                       }
                    global_commands={
                                     'ExitCLI':{'description':'Exit the toolkit command line interface.',
                                                'CLI_syntax':'X',
                                                'allowed_variations':['ExitCLI','x','X','exit()','exit','EXIT','esc','ESC','/exit','/EXIT','/X','/x','x()','X()'], # references allowed variations for input arguments to trigger this command
                                                'details':None},
                                     'ReturnToHomePage':{'description':'Return to the home view on the CLI',
                                                         'CLI_syntax':'H',
                                                         'allowed_variations':['ReturnToHomePage','h','H','home','home','/home','home()','/h','/H'],
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
                                     'TeleportToSpecifiedPath':{'description':'Shifts the CLI window to a view at the path str or the name of the file. This ideally == the full path str.',
                                                               'CLI_syntax':'BK',
                                                               'allowed_variations':['TeleportToSpecifiedPath --id [ID]','/TeleportToSpecifiedPath --id [ID]', 'TP --id [ID]','tp --id [ID]', 'chdir --id [ID]', 'cd --id [ID]', 'cd --id [ID]', '/tp PATH', '/tp --id [ID]','/TP --id [ID]','/TP --id [ID]','teleport(--id [ID])','tp(--id [ID])'],
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
                                     'SaveCurrentPathAsBookmark':{'description':'Saves the directory path associated with the current interface window as a bookmark. Running this command will prompt a second input for the bookmark name unless it == also specified in the first call.',
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
                                       'path_commands':path_commands,
                                       'manual_commands':manual_commands
                                       }
                    with open(self.cmd_metadata_path, "w") as outfile:
                        json.dump(commands_metadata, outfile)
                self.cmd_metadata=commands_metadata

            def __init_core():
                self.POWER=True
                self.about={'Author':author,'Version':version,'Created':created}
                self.width_limit=width_limit
                self.height_limit=height_limit
                manual_override_mode=self.__check_manual_override_credentials(manual_override_pwd)
                self.CLI={
                          'cwd':(self.current_settings['homePathString']) if (jump_to_path == None) else jump_to_path,
                          'mode':'home',
                          'back_cache':[], # !!! NOTE: 0 INDEX IS MOST RECENT FOR NAVIGATION CACHES !!!
                          'forward_cache':[], # !!! NOTE: 0 INDEX IS MOST RECENT FOR NAVIGATION CACHES !!!
                          'manual_override_mode':manual_override_mode,
                          'exec_str':'',
                          'about':{'Author':author,'Version':version,'Created':created}
                         }
                self.sys_os, self.sys_slashes=__os_syntax_profiling()
                self.src_dir_path=__establish_paths(src_dir_path)
                self.bookmarks_path=self.src_dir_path + self.sys_slashes + 'bookmarks.json'
                self.usage_data_path=self.src_dir_path + self.sys_slashes + 'usage_data.json'
                self.default_settings_path=self.src_dir_path + self.sys_slashes + 'default_settings.json'
                self.current_settings_path=self.src_dir_path + self.sys_slashes + 'current_settings.json'
                self.cmd_metadata_path=self.src_dir_path + self.sys_slashes +  'commands.json'
                self.bookmarks=__load_bookmarks()
                self.usage_data=__load_usage_data()
                self.cmd_metadata=__load_cmd_metadata()
                self.default_settings=__load_default_settings()
                self.current_settings=__load_current_settings()
                self.dividers=__load_dividers()
                self.session_log={'timestamps':[self.__obtain_fmt_datetime_as_str(), None],'saved_str_blocks':[]}
                while self.POWER:
                    os.chdir(self.CLI['cwd'])
                    self.__CLI_display()
                    CLI_input=input()
                    self.__CLI_cmd(CLI_input)
            __init_core(**kwargs)

    dtk_cli_obj_instance=DTK_CLI()

################################################################
### main() FUNCTION CALLED VIA OPENING FILE THROUGH TERMINAL ###
################################################################
if __name__=='__main__':
    main()
