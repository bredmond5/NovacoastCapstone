from datetime import datetime

from dms.groups.models import Group
from dms.domains.models import Domain
from dms.lookalikes.models import Lookalike


def test_index(client, session):
    groups = [
        Group(name='Joe Bloggs', emails='jbloggs@example.com'),
        Group(
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com'
        ),
    ]
    domains = [
        Domain(id=1, name='www.example.com', group=groups[0]),
        Domain(id=2, name='www.newdomain.com', group=groups[1]),
    ]
    lookalikes = [
        Lookalike(
            name='www.exampl.com',
            domain_id=1,
            ip_address='33.33.33.33',
            creation_date=datetime(2020, 9, 1)
        ),
        Lookalike(
            name='www.nuwdomain.com',
            domain_id=2,
            ip_address='34.34.34.34'
        ),
        Lookalike(
            name='www.newdoman.com',
            domain_id=2,
            ip_address='34.34.34.35',
            creation_date=datetime(2020, 9, 2)
        ),
    ]
    session.add_all(groups)
    session.add_all(domains)
    session.add_all(lookalikes)
    session.commit()
    res = client.get('/lookalikes/')
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 3
    results = data['results']
    assert any(
        lookalike['name'] == 'www.exampl.com'
        and lookalike['domainId'] == 1
        and lookalike['ipAddress'] == '33.33.33.33'
        and lookalike['creationDate'] == '2020-09-01T00:00:00'
        for lookalike in results
    )
    assert any(
        lookalike['name'] == 'www.nuwdomain.com'
        and lookalike['domainId'] == 2
        and lookalike['ipAddress'] == '34.34.34.34'
        and lookalike['creationDate'] is None
        for lookalike in results
    )
    assert any(
        lookalike['name'] == 'www.newdoman.com'
        and lookalike['domainId'] == 2
        and lookalike['ipAddress'] == '34.34.34.35'
        and lookalike['creationDate'] == '2020-09-02T00:00:00'
        for lookalike in results
    )
    assert all('foundOn' in result for result in data['results'])
    assert all('updatedAt' in result for result in data['results'])


def test_get(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.add(Lookalike(
        name='www.exampl.com',
        domain_id=1,
        ip_address='33.33.33.33',
        creation_date=datetime(2020, 9, 1)
    ))
    session.commit()
    res = client.get('/lookalikes/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == 'www.exampl.com'
    assert data['domainId'] == 1
    assert data['ipAddress'] == '33.33.33.33'
    assert data['creationDate'] == '2020-09-01T00:00:00'
    assert 'foundOn' in data
    assert 'updatedAt' in data


def test_get_nonexistent(client, session):
    res = client.get('/lookalikes/1')
    assert res.status_code == 404
