#!/usr/bin/env python
# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <tsuyoshi.hombashi@gmail.com>
"""

from __future__ import absolute_import, print_function

import errno
import sys

import logbook
import subprocrunner as spr

from .__version__ import __version__
from ._argparse_wrapper import ArgparseWrapper
from ._capabilities import check_execution_authority
from ._common import initialize_cli, is_execute_tc_command, normalize_tc_value
from ._const import Tc, TcCommandOutput, TcSubCommand
from ._error import NetworkInterfaceNotFoundError
from ._logger import logger, set_logger
from ._network import verify_network_interface
from ._tc_script import write_tc_script
from .traffic_control import TrafficControl


def parse_option():
    parser = ArgparseWrapper(__version__)

    group = parser.parser.add_argument_group("Traffic Control")
    if set(["-d", "--device"]).intersection(set(sys.argv)):
        # [deprecated] for backward compatibility
        group.add_argument("-d", "--device", required=True, help="network device name (e.g. eth0)")
    else:
        group.add_argument("device", help="network device name (e.g. eth0)")
    group.add_argument(
        "-a",
        "--all",
        dest="is_delete_all",
        action="store_true",
        help="delete all of the shaping rules.",
    )
    group.add_argument(
        "--id",
        dest="filter_id",
        help="""delete a shaping rule which has a specific id. you can get an id (filter_id)
        by tcshow command output.
        e.g. "filter_id": "800::801"
        """,
    )

    parser.add_routing_group()

    return parser.parser.parse_args()


def create_tc_obj(options):
    from .parser.shaping_rule import TcShapingRuleParser
    from simplesqlite.query import Where

    if options.filter_id:
        ip_version = 6 if options.is_ipv6 else 4
        shaping_rule_parser = TcShapingRuleParser(
            device=options.device,
            ip_version=ip_version,
            tc_command_output=options.tc_command_output,
            logger=logger,
        )
        shaping_rule_parser.parse()
        result = shaping_rule_parser.con.select_as_dict(
            table_name=TcSubCommand.FILTER.value,
            column_list=[
                Tc.Param.SRC_NETWORK,
                Tc.Param.DST_NETWORK,
                Tc.Param.SRC_PORT,
                Tc.Param.DST_PORT,
            ],
            where=Where(Tc.Param.FILTER_ID, options.filter_id),
        )
        if not result:
            logger.error(
                "shaping rule not found associated with the id ({}).".format(options.filter_id)
            )
            sys.exit(1)

        filter_param = result[0]
        dst_network = filter_param.get(Tc.Param.DST_NETWORK)
        src_network = filter_param.get(Tc.Param.SRC_NETWORK)
        dst_port = filter_param.get(Tc.Param.DST_PORT)
        src_port = filter_param.get(Tc.Param.SRC_PORT)
    else:
        dst_network = options.dst_network
        src_network = options.src_network
        dst_port = options.dst_port
        src_port = options.src_port

    return TrafficControl(
        options.device,
        direction=options.direction,
        dst_network=dst_network,
        src_network=src_network,
        dst_port=dst_port,
        src_port=src_port,
        is_ipv6=options.is_ipv6,
    )


def main():
    options = parse_option()

    initialize_cli(options)

    if is_execute_tc_command(options.tc_command_output):
        check_execution_authority("tc")

        is_delete_all = options.is_delete_all
    else:
        spr.SubprocessRunner.default_is_dry_run = True
        is_delete_all = True
        set_logger(False)

    try:
        verify_network_interface(options.device)
    except NetworkInterfaceNotFoundError as e:
        logger.error(e)
        return errno.EINVAL

    spr.SubprocessRunner.clear_history()
    tc = create_tc_obj(options)
    if options.log_level == logbook.INFO:
        spr.set_log_level(logbook.ERROR)
    normalize_tc_value(tc)

    return_code = 0
    try:
        if is_delete_all:
            return_code = tc.delete_all_tc()
        else:
            return_code = tc.delete_tc()
    except NetworkInterfaceNotFoundError as e:
        logger.error(e)
        return errno.EINVAL

    command_history = "\n".join(tc.get_command_history())

    if options.tc_command_output == TcCommandOutput.STDOUT:
        print(command_history)
        return return_code
    elif options.tc_command_output == TcCommandOutput.SCRIPT:
        set_logger(True)
        write_tc_script(Tc.Command.TCDEL, command_history, filename_suffix=options.device)
        return return_code

    logger.debug("command history\n{}".format(command_history))

    return return_code


if __name__ == "__main__":
    sys.exit(main())
