from io import BytesIO
from time import sleep
from unittest import mock

from dms.domains.models import Domain
from dms.groups.models import Group


def test_model_updated_at_field(session):
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
    )
    domain = Domain(name='www.example.com', group=group)
    session.add(group)
    session.add(domain)
    session.commit()
    old_updated_at = domain.updated_at
    sleep(1)
    domain.active = False
    session.commit()
    new_updated_at = Domain.query.get(domain.id).updated_at
    assert old_updated_at < new_updated_at


def test_index(client, session):
    groups = [
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com',
        ),
    ]
    domains = [
        Domain(name='www.example.com', group=groups[0]),
        Domain(name='www.example.co.uk', group=groups[0]),
        Domain(name='www.legends.com', group=groups[1]),
    ]
    session.add_all(groups)
    session.add_all(domains)
    session.commit()
    res = client.get('/domains/')
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == len(domains)
    for dom in domains:
        assert any(
            result['name'] == dom.name
            and result['groupId'] == dom.group_id
            for result in data['results']
        )
    assert all('createdAt' in result for result in data['results'])
    assert all('updatedAt' in result for result in data['results'])
    assert all(result['active'] is True for result in data['results'])
    assert all(result['lastScanned'] is None for result in data['results'])
    assert all(result['numberOfScans'] == 0 for result in data['results'])


def test_index_search(client, session):
    groups = [
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com',
        ),
    ]
    domains = [
        Domain(name='www.example.com', group=groups[0]),
        Domain(name='www.example.co.uk', group=groups[0]),
        Domain(name='www.legends.com', group=groups[1]),
    ]
    session.add_all(groups)
    session.add_all(domains)
    session.commit()
    res = client.get('/domains/', json={'q': 'example'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 2
    results = data['results']
    assert any(
        domain['name'] == 'www.example.com'
        for domain in results
    )
    assert any(
        domain['name'] == 'www.example.co.uk'
        for domain in results
    )


def test_index_search_bogus_string(client, session):
    groups = [
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com',
        ),
    ]
    domains = [
        Domain(name='www.example.com', group=groups[0]),
        Domain(name='www.example.co.uk', group=groups[0]),
        Domain(name='www.legends.com', group=groups[1]),
    ]
    session.add_all(groups)
    session.add_all(domains)
    session.commit()
    res = client.get('/domains/', json={'q': 'bogus'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 0


def test_get(client, session):
    g = Group(name='Joe Bloggs', emails='jbloggs@example.com')
    session.add(g)
    session.add(Domain(id=1, name='www.example.com', group=g))
    session.commit()
    res = client.get('/domains/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['name'] == 'www.example.com' and data['groupId'] == g.id
    assert data['active'] is True
    assert data['lastScanned'] is None
    assert data['numberOfScans'] == 0


def test_get_nonexistent(client, session):
    nonexistent_id = 2
    assert Domain.query.get(nonexistent_id) is None
    res = client.get(f'/domains/{nonexistent_id}')
    assert res.status_code == 404


@mock.patch('dms.domains.routes.logger.info')
def test_create(log_info, client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.commit()
    res = client.post('/domains/', json={
        'name': 'www.example.com',
        'groupId': 1,
    })
    assert res.status_code == 201
    data = res.get_json()
    q = Domain.query.filter_by(
        id=data['id'], name='www.example.com', group_id=1)
    assert q.count() == 1
    log_info.assert_called_with(
        f"Created new domain: <Domain {data['id']} \"www.example.com\">"
    )


def test_create_with_active_false(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.commit()
    res = client.post('/domains/', json={
        'name': 'www.example.com',
        'groupId': 1,
        'active': False,
    })
    assert res.status_code == 201
    data = res.get_json()
    q = Domain.query.filter_by(
        id=data['id'],
        name='www.example.com',
        group_id=1,
        active=False
    )
    assert q.count() == 1


def test_create_no_name(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.commit()
    assert Domain.query.count() == 0  # assert is empty
    res = client.post('/domains/', json={'groupId': 1})
    assert res.status_code == 400
    assert Domain.query.count() == 0  # assert is still empty


def test_create_no_group_id(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.commit()
    assert Domain.query.count() == 0  # assert is empty
    res = client.post('/domains/', json={'name': 'www.example.com'})
    assert res.status_code == 400
    assert Domain.query.count() == 0  # assert is still empty


@mock.patch('dms.domains.routes.logger.info')
def test_update(log_info, client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.add(Group(id=2, name='Ada Begg', emails='abegg@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.commit()
    res = client.put(
        '/domains/1',
        json={'name': 'www.example.co.uk', 'groupId': 2}
    )
    assert res.status_code == 200
    dom = Domain.query.get(1)
    assert dom.name == 'www.example.co.uk' and dom.group_id == 2
    log_info.assert_called_with(
        'Updated domain: <Domain 1 "www.example.co.uk">'
    )


def test_update_with_active_false(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.commit()
    res = client.put(
        '/domains/1',
        json={
            'active': False
        }
    )
    assert res.status_code == 200
    dom = Domain.query.get(1)
    assert dom.name == 'www.example.com' and dom.group_id == 1
    assert dom.active is False


def test_update_no_name(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.add(Group(id=2, name='Ada Begg', emails='abegg@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.commit()
    res = client.put(
        '/domains/1',
        json={'groupId': 2}
    )
    assert res.status_code == 200
    dom = Domain.query.get(1)
    assert dom.name == 'www.example.com' and dom.group_id == 2


def test_update_no_group_id(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.commit()
    res = client.put(
        '/domains/1',
        json={'name': 'www.example.co.uk'}
    )
    assert res.status_code == 200
    dom = Domain.query.get(1)
    assert dom.name == 'www.example.co.uk' and dom.group_id == 1


@mock.patch('dms.domains.routes.logger.info')
def test_delete(log_info, client, session):
    session.add(Group(id=1, name='John Doe', emails='jdoe@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.commit()
    res = client.delete('/domains/1')
    assert res.status_code == 200
    assert Domain.query.get(1) is None
    log_info.assert_called_with(
        'Deleted domain: <Domain 1 "www.example.com">'
    )


def test_delete_nonexistent(client, session):
    session.add(Group(id=1, name='John Doe', emails='jdoe@example.com'))
    session.add(Domain(id=1, name='www.example.com', group_id=1))
    session.commit()
    nonexistent_id = 2
    assert Domain.query.get(nonexistent_id) is None
    res = client.delete(f'/domains/{nonexistent_id}')
    assert res.status_code == 404
    assert Domain.query.count() == 1


TEST_DOMAINS_CSV = b"""name,group_id
www.example.com,1
www.legends.com,2
"""


def test_import_csv(client, session):
    session.add_all([
        Group(
            id=1,
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            id=2,
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com',
        ),
    ])
    res = client.post(
        '/domains/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={
            'file': (BytesIO(TEST_DOMAINS_CSV), 'test_domains.csv')
        }
    )
    assert res.status_code == 200

    def domains_exists(name, group_id):
        return Domain.query.filter_by(
            name=name,
            group_id=group_id
        ).count() == 1

    assert domains_exists('www.example.com', 1)
    assert domains_exists('www.legends.com', 2)


def test_import_csv_wrong_extension(client, session):
    res = client.post(
        '/domains/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={
            'file': (BytesIO(TEST_DOMAINS_CSV), 'test_domains.txt')
        }
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['message'] == "Invalid file extension"


def test_import_csv_no_file(client, session):
    res = client.post(
        '/domains/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={}
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['message'] == "No file in data"


def test_import_csv_no_filename(client, session):
    res = client.post(
        '/domains/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={
            'file': (BytesIO(TEST_DOMAINS_CSV), '')
        }
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['message'] == "No file selected"
