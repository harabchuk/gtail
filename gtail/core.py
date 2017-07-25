import tailhead
import sys
from gelfclient import UdpClient
from optparse import OptionParser
import re
import datetime
import time


__version__ = '0.0.1'

LOG_PATTERN = "(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) \[(?P<level>.+)\] (?P<message>.+)"


class DummyGelf():

    def log(self, obj):
        print obj


def follow(log_file_path, sleep=1.0, send_func=None):
    try:
        for l in tailhead.follow_path(log_file_path):
            if l is not None:
                send_func(l)
            else:
                time.sleep(sleep)
    except KeyboardInterrupt:
        pass


def regex_parse(line, pattern):
    default = {'message': line, 'datetime': '', 'level': 'INFO'}
    try:
        f = re.search(pattern, line)
        if not f:
            return default
        else:
            result = f.groupdict()
            if result.get('datetime'):
                dt = datetime.datetime.strptime(result.get('datetime'), '%Y-%m-%d %H:%M:%S,%f')
                result['datetime'] = time.mktime(dt.timetuple())
            return result
    except:
        return default


def send_gray_log(line, gelf, parse_func=None):
    if parse_func is not None:
        gelf.log(parse_func(line))
    else:
        gelf.log(line)


def parse_options():
    cmdline = OptionParser(usage="usage: %prog [options] logfile", description="Send log file lines to the GrayLog2")
    cmdline.add_option("--version", action="store_true", help="Print version and exit.")
    cmdline.add_option("--sleep", type=float, default=1.0,  action="store", help="Delay, default=1.0 sec.")
    cmdline.add_option("--graylog-host", default='localhost',  action="store", help="GrayLog Server, default=localhost")
    cmdline.add_option("--graylog-port", default='12202',  action="store", help="GrayLog Port, default=12202")
    cmdline.add_option("--source",  action="store", default='gtail', help="source filed value")
    cmdline.add_option("--dry-run",  action="store_true", default=False, help="source filed value")
    result = list(cmdline.parse_args())
    result.append(cmdline)
    return result


def get_gelf(host, port, source):
    return UdpClient(host, port=port, source=source)

if __name__ == '__main__':

    options, args, cmdline = parse_options()

    if options.version:
        print "gtail version", __version__
        sys.exit(0)

    if len(args) != 1:
        cmdline.error("Please provide a logfile to read.")

    if not options.dry_run:
        gelf = get_gelf(options.graylog_host, options.graylog_port, options.source)
    else:
        gelf = DummyGelf()

    pattern = re.compile(LOG_PATTERN)

    follow(args[0], options.sleep, lambda line: send_gray_log(line, gelf, lambda l: regex_parse(l, pattern)))
