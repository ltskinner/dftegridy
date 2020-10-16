
import sys

import io
import json
import yaml

import numpy as np
import pandas as pd
from collections import OrderedDict

from . import dunits


class DFID(object):
    def __init__(self, dunit_config=None):
        self.dunit_config = dunit_config

        self.dfid_profile = None
        self.dfid_report = None
    
    def set_dunit_config(self, dunit_config):
        self.dunit_config = dunit_config

    def save_dunit_config(self, outfile_path):
        # TODO
        pass

    def load_dunit_config(self, infile_path):
        # TODO
        pass

    @staticmethod
    def _confirm_dunit_config(dunit_config):
        # tested
        # TODO: Add other dict{} check stuff as well
        if dunit_config is None:
            msg = '\n'.join([
                'dunit_config not yet specified - please set the config via:',
                '    - dfid = DFID(dunit_config=dunit_config)'
                '    - dfid.set_dfid_config(dfid_config)'
            ])
            raise ValueError(msg)
        return True

    def profile(self, df):
        self._confirm_dunit_config(self.dunit_config)

        self.dfid_profile = {}

        for col in df.columns:
            data = df[col]

            dtype = str(df[col].dtype)
            hasna = bool(df[col].isnull().values.any())

            record = {
                'dtype': dtype,
                'hasna': hasna,
            }

            if col in self.dunit_config.keys():
                dunit_name = self.dunit_config[col]
                record['dunit'] = dunit_name

                dunit_obj = dunits.get_dunit_obj(dunit_name, col)

                values_profile = dunit_obj.profile(data)
                for key, value in values_profile.items():
                    record[key] = value
            else:
                dunit_name = dunits.UNVERIFIED
                record['dunit'] = dunit_name

            self.dfid_profile[col] = record
        
        return self.dfid_profile

    @staticmethod
    def _clean_dict_structure(ordered_dict):
        def convert(o):
            if isinstance(o, np.generic): return o.item()  
            raise TypeError

        dfid_ordered_records = []
        for col, record in ordered_dict.items():
            dfid_ordered_records.append((col, record))

        dfid_profile_ordered = OrderedDict(dfid_ordered_records)

        dfid_profile_str = json.dumps(dfid_profile_ordered, default=convert)
        dfid_clean_dict = json.loads(dfid_profile_str)
        return dfid_clean_dict

    def save_profile(self, dfid_profile_path):
        dfid_clean_dict = self._clean_dict_structure(self.dfid_profile)

        with io.open(dfid_profile_path, 'w', encoding='utf8') as outfile:
            yaml.dump(dfid_clean_dict, outfile,
                      default_flow_style=False,
                      #allow_unicode=True,  # Dont care about this right now
                      sort_keys=False)

    def print_profile(self):
        # notest - cosmetic
        print('~~~~ DFID Profile ~~~~')
        dfid_clean_dict = self._clean_dict_structure(self.dfid_profile)
        out_stream = sys.stdout
        yaml.dump(dfid_clean_dict, out_stream,
                  default_flow_style=False,
                  #allow_unicode=True,  # Dont care about this right now
                  sort_keys=False)

    def load_profile(self, dfid_profile_path):
        with open(dfid_profile_path, 'r') as stream:
            self.dfid_profile = yaml.safe_load(stream)

    def _verify_no_extra_cols(self, df):
        error_report = []
        for col in df.columns:
            if col not in self.dfid_profile.keys():
                error = {
                    'level': 'info',
                    'msg': f'New column added'
                }
                error_report.append(error)

        return error_report

    def _verify_has_expected_cols(self, df):
        error_report = []
        for key in self.dfid_profile.keys():
            if key not in df.columns:
                error = {
                    'level': 'critical',
                    'msg': f'Missing column: {key}'
                }
                error_report.append(error)
        
        return error_report

    def _verify_cols_present(self, df):
        error_report = []
        extra_report = self._verify_no_extra_cols(df)
        expected_report = self._verify_has_expected_cols(df)
        error_report.extend(extra_report)
        error_report.extend(expected_report)
        return error_report

    def _verify_cols_order(self, df):
        expected_order = [
            col for col in self.dfid_profile.keys()
        ]
        actual_order = df.columns.tolist()

        error_report = []
        if expected_order != actual_order:
            msg = '\n'.join([
                f'Expected column order != new column order',
                f'    - Disregard if column order does not matter'
            ])
            error = {
                'level': 'info',
                'msg': msg
            }
            error_report.append(error)
        
        return error_report

    def _verify_columns(self, df):
        error_report = []
        present_report = self._verify_cols_present(df)
        order_report = self._verify_cols_order(df)

        error_report.extend(present_report)
        error_report.extend(order_report)
        return error_report

    def verify(self, df, skip_unverified=False):
        # TODO: confirm has profile to work with

        self.dfid_report = {}

        cols_report = self._verify_columns(df)
        self.dfid_report['columns'] = cols_report

        for column, profile in self.dfid_profile.items():
            if column not in df.columns:
                self.dfid_report[column] = [{
                    'level': 'critical',
                    'msg': f'[!] Missing column: `{column}` - unable to verify [!]'
                }]
                continue

            data = df[column]

            dunit = profile['dunit']
            if dunit == dunits.UNVERIFIED:
                if not skip_unverified:
                    self.dfid_report[column] = [{
                        'level': 'info',
                        'msg': dunits.UNVERIFIED
                    }]
                continue

            dunit_obj = dunits.get_dunit_obj(dunit, column)

            values_report = dunit_obj.verify(data, profile)
            dtype_report = dunit_obj.verify_dtype(data, profile)
            na_report = dunit_obj.verify_na(data, profile)

            column_reports = []
            column_reports.extend(values_report)
            column_reports.extend(dtype_report)
            column_reports.extend(na_report)

            if len(column_reports) > 0:
                self.dfid_report[column] = column_reports

        return self.dfid_report
    
    def print_verification_report(self):
        # notest, this is going to change
        print('~~~~ DFID Verification Report ~~~~')
        '''
        dfid_clean_dict = self._clean_dict_structure(self.dfid_report)
        out_stream = sys.stdout
        yaml.dump(dfid_clean_dict, out_stream,
                  default_flow_style=False,
                  #allow_unicode=True,  # Dont care about this right now
                  sort_keys=False)
        '''
        for key, value in self.dfid_report.items():
            print(f'--> {key}:')
            for error in value:
                for error_key, error_msg in error.items():
                    print(f'{error_msg}')
            print()
