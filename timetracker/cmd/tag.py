"""List the location of the csv file(s)"""

__copyright__ = 'Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.'
__author__ = "DV Klopfenstein, PhD"

#from os.path import dirname
#from os.path import exists
from logging import debug
from timetracker.utils import yellow
#from timetracker.cfg.cfg import Cfg
#from timetracker.cfg.utils import get_filename_globalcfg
#from timetracker.cfg.cfg_global import CfgGlobal
#from timetracker.msgs import str_init


def cli_run_tag(fnamecfg, args):
    """Stop the timer and record this time unit"""
    run_tag(fnamecfg, args.global_config_file)

def run_tag(fcfg_local, fcfg_global, dirhome=None):
    """Stop the timer and record this time unit"""
    # Get the starting time, if the timer is running
    debug(yellow('RUNNING COMMAND TAG'))
    assert fcfg_local
    assert fcfg_global
    assert dirhome
    #cfg = Cfg(fcfg_local)  #### , fcfg_global, dirhome)
    #assert cfg
    print('The `tag` command is coming soon. If you need it sooner, open an issue at:')
    print('https://github.com/dvklopfenstein/timetracker/issues/new/choose')
    # pylint: disable=line-too-long
    #filename_globalcfg = get_filename_globalcfg(dirhome, fcfg_global, fcfg_doc) if file is None else file
    #if not exists(filename_globalcfg):
    #    print(str_init(fcfg_local))
    #    return
    #cfg_global = CfgGlobal(filename_globalcfg)
    #tag = cfg_global.get_tag()
    #if tag is None:
    #    print(str_init(print(str_init(fcfg_local))))
    #for proj, fcfgloc in sorted(tag):
    #    print(f'{proj:26} {dirname(dirname(fcfgloc))}')


    #cfg = Cfg(fcfg_local, fcfg_global)

#    if not exists(fnamecfg):
#        run_tag_global(uname)
#    cfgproj = CfgProj(fnamecfg, dirhome=dirhome)
#
#    # List location of the timetracker file with this time unit
#    if uname == 'all':
#        _get_proj_all(cfgproj)
#    else:
#        _get_proj_user(cfgproj, uname)
#
#def _get_proj_user(cfgproj, uname):
#    fcsv = cfgproj.get_filename_csv(uname)
#    if fcsv is not None:
#        print(f'CSV exists({int(exists(fcsv))}) {fcsv}')
#
#def _get_proj_all(cfgproj, dirhome):
#    fcsvs = cfgproj.get_filenames_csv(dirhome)
#    for fcsv in fcsvs:
#        if fcsv is not None:
#            print(f'CSV exists({int(exists(fcsv))}) {fcsv}')
#
#def _run_cfg_global(dirhome):
#    cfg_global = CfgGlobal(dirhome)
#    assert cfg_global
#
#
#def run_tag_global(uname):
#    print(filename_globalcfg)


# Copyright (C) 2025-present, DV Klopfenstein, PhD. All rights reserved.
