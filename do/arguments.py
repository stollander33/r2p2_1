# -*- coding: utf-8 -*-

import os
import sys
import argparse
from do.utils.myyaml import load_yaml_file
from do import ABSOLUTE_PATH

parse_conf = load_yaml_file('argparser', path=ABSOLUTE_PATH, logger=False)

# Arguments definition
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description=parse_conf.get('description')
)

# PARAMETERS
for option_name, option in parse_conf.get('options', {}).items():
    option_type = str
    if option.get('type') == 'bool':
        option_type = bool
    default = option.get('default')
    # myhelp = f"{option.get('help')} [default: {default}]"
    myhelp = "%s [default: %s]" % (option.get('help'), default)
    parser.add_argument(
        '--%s' % option_name, type=option_type,
        metavar=option.get('metavalue'), default=default, help=myhelp
    )

# COMMANDS
main_command = parse_conf.get('command')
subparsers = parser.add_subparsers(
    dest=main_command.get('name'),
    help=main_command.get('help')
)
subparsers.required = True

for command_name, options in parse_conf.get('subcommands', {}).items():
    subparse = subparsers.add_parser(
        command_name, help=options.get('description'))

    controlcommands = options.get('controlcommands', {})
    if len(controlcommands) > 0:
        innerparser = subparse.add_subparsers(
            dest='controlcommand'
        )
        innerparser.required = options.get('controlrequired', False)
        for subcommand, suboptions in controlcommands.items():
            subcommand_help = suboptions.pop(0)
            innerparser.add_parser(subcommand, help=subcommand_help)

# Reading input parameters
current_args = parser.parse_args()
current_args = vars(current_args)

# Log level
os.environ['DEBUG_LEVEL'] = current_args.get('log_level')

if True:
    from do.utils.logs import get_logger
    log = get_logger(__name__)
    log.verbose("Parsed arguments: %s" % current_args)