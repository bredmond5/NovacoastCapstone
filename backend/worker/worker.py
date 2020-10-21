import logging
import os
import subprocess

import pika

# Get configuration from environment variables
queue = os.getenv('WORKER_RABBITMQ_QUEUE', 'scans')
host = os.getenv('WORKER_RABBITMQ_HOST', 'rabbitmq')
log_level = os.getenv('WORKER_LOG_LEVEL', 'INFO').upper()

logging.basicConfig(
    format='%(asctime)s - %(lineno)d - %(levelname)s - %(message)s',
    level=log_level,
)

logger = logging.getLogger(__name__)


class DnstwistError(Exception):
    """Exception raised when dnstwist fails with an error.
    """
    pass


def dnstwist(domain_name: str) -> str:
    """Calls the dnstwist program to find registered permutations of domain_name.

    The dnstwist program is a command line utility that is expected to be
    installed and in the system's PATH. When run using this command,
    dnstwist is executed with the following arguments:

        dnstwist -f csv -agmrws <domain_name>

    The return value of this function is the output of the command as a string.
    The output is in CSV format. An example of the output follows:

        fuzzer,domain-name,dns-a,dns-aaaa,dns-mx,dns-ns,geoip-country,whois-created,ssdeep-score
        original*,example.com,93.184.216.34,2606:2800:220:1:248:1893:25c8:1946,,a.iana-servers.net;b.iana-servers.net,United States,,
        addition,examplea.com,23.20.239.12,,,nsg1.namebrightdns.com;nsg2.namebrightdns.com,United States,,
        addition,exampleb.com,23.20.239.12,,,ns1.namebrightdns.com;ns2.namebrightdns.com,United States,,
        addition,examplec.com,23.20.239.12,,,nsg1.namebrightdns.com;nsg2.namebrightdns.com,United States,,

    Note that the first line of the output is a CSV header and the second line is the
    information for domain_name.

    Args:
        domain_name (str): the domain to scan for permutations

    Returns:
        str: the output of the command
    """
    result = subprocess.run(
        ['dnstwist', '-f', 'csv', '-grwm', domain_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise DnstwistError(result.stderr)
    else:
        return result.stdout


class Lookalike():
    # You will need to add the following fields for this class:
    #   * name
    #   * ip_address
    #   * creation_date

    def __init__(self, name, ip_address, creation_date):
        # TODO: implement this
        pass

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __repr__(self):
        return f'<Lookalike {self.name}, {self.ip_address}, {self.creation_date}>'


def scan_domain(domain_name: str) -> list[Lookalike]:
    """Returns lookalike domains registered to names similar to domain_name.

    Example:

    > scan_domain('example.com')
    [<Lookalike examplea.com, 23.20.239.12, >, <Lookalike exampleb.com, 23.20.239.12, >]

    Args:
        domain_name (str): the name of the domain to scan, e.g. 'example.com'

    Returns:
        list[Lookalike]: the list of lookalike domains
    """
    # TODO: implement this
    #
    # HINTS:
    # - Use the dnstwist function to get the similar domains in CSV format
    # - You can use the csv module from the Python standard library to parse
    #   the data
    # - You will need to ignore the first non-header line of CSV data because
    #   that data is about the original domain
    # - You will also need to implement the Lookalike class
    return []


def on_message(channel, method, properties, body):
    """Called when a scan job message is received.
    """
    logger.debug(
        f'Recieved message('
        f'channel={channel}, '
        f'method={method}, '
        f'properties={properties}, '
        f'body={body})'
    )


if __name__ == "__main__":
    # Listen to messages from RabbitMQ
    logger.info('Worker starting...')
    params = pika.ConnectionParameters(host=host, heartbeat=0)
    try:
        con = pika.BlockingConnection(params)
        channel = con.channel()
        channel.queue_declare(queue)
        channel.basic_consume(queue, on_message)
    finally:
        if channel.is_open:
            channel.close()
            logger.debug('Channel closed')
        if con.is_open:
            con.close()
            logger.debug('Connection closed')
