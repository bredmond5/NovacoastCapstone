from unittest import mock

from . import worker

EXAMPLE_NO_RESULTS = """fuzzer,domain-name,dns-a,dns-aaaa,dns-mx,dns-ns,geoip-country,whois-created,ssdeep-score
original*,example.com,93.184.216.34,2606:2800:220:1:248:1893:25c8:1946,,a.iana-servers.net;b.iana-servers.net,United States,,
"""

EXAMPLE_RESULTS = """fuzzer,domain-name,dns-a,dns-aaaa,dns-mx,dns-ns,geoip-country,whois-created,ssdeep-score
original*,example.com,93.184.216.34,2606:2800:220:1:248:1893:25c8:1946,,a.iana-servers.net;b.iana-servers.net,United States,,
addition,examplea.com,23.20.239.12,,,nsg1.namebrightdns.com;nsg2.namebrightdns.com,United States,,
addition,exampleb.com,23.20.239.12,,,ns1.namebrightdns.com;ns2.namebrightdns.com,United States,,
"""


def test_scan_domain_no_results():
    worker.dnstwist = mock.Mock()
    worker.dnstwist.return_value = EXAMPLE_NO_RESULTS

    lookalikes = worker.scan_domain('example.com')
    assert lookalikes == []


def test_scan_domain_many_results():
    worker.dnstwist = mock.Mock()
    worker.dnstwist.return_value = EXAMPLE_RESULTS

    lookalikes = worker.scan_domain('example.com')
    assert len(lookalikes) == 2
    assert any(
        lookalike == worker.Lookalike('examplea.com', '23.20.239.12', '')
        for lookalike in lookalikes
    )
    assert any(
        lookalike == worker.Lookalike('exampleb.com', '23.20.239.12', '')
        for lookalike in lookalikes
    )
