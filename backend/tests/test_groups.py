from datetime import datetime, timedelta
from io import BytesIO
from time import sleep
from unittest import mock

import pytest

from dms.groups.models import Group


def test_model_update_recur_with_bogus(session):
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
    )
    with pytest.raises(ValueError):
        group.recur = 'bogus'


def test_model_update_time_zone_with_bogus(session):
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
    )
    with pytest.raises(ValueError):
        group.time_zone = 'bogus'


def test_model_updated_at_field(session):
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
    )
    session.add(group)
    session.commit()
    old_updated_at = group.updated_at
    sleep(1)
    group.name = 'testing'
    session.commit()
    new_updated_at = Group.query.get(group.id).updated_at
    assert old_updated_at < new_updated_at


def test_index(client, session):
    session.add_all([
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com',
        ),
        Group(
            name='Ada Begg',
            emails='abegg@example.com',
        ),
    ])
    session.commit()
    res = client.get('/groups/')
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 3
    results = data['results']
    assert any(group['emails'] == 'jbloggs@example.com'
               and group['name'] == 'Joe Bloggs'
               for group in results)
    assert any(group['emails'] == 'jdoe@example.com;jappleseed@legends.com'
               and group['name'] == 'Example, Inc.'
               for group in results)
    assert any(group['emails'] == 'abegg@example.com'
               and group['name'] == 'Ada Begg'
               for group in results)
    assert all('createdAt' in group for group in results)
    assert all('updatedAt' in group for group in results)
    assert all(result['recur'] == 'daily' for result in results)
    assert all(result['timeZone'] == 'UTC' for result in results)
    assert all('startAt' in result for result in results)


def test_index_search_name(client, session):
    session.add_all([
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='jdoe@example.com;jappleseed@legends.com',
        ),
        Group(
            name='Ada Begg',
            emails='abegg@example.com',
        ),
    ])
    session.commit()
    res = client.get('/groups/', json={'q': 'Joe Bloggs'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 1
    result = data['results'][0]
    assert result['name'] == 'Joe Bloggs'
    assert result['emails'] == 'jbloggs@example.com'


def test_index_search_emails(client, session):
    session.add_all([
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='abegg@example.com;jappleseed@legends.com',
        ),
        Group(
            name='Ada Begg',
            emails='abegg@example.com',
        ),
    ])
    session.commit()
    res = client.get('/groups/', json={'q': 'abegg'})
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 2
    results = data['results']
    assert any(
        group['name'] == 'Example, Inc.'
        and group['emails'] == 'abegg@example.com;jappleseed@legends.com'
        for group in results
    )
    assert any(
        group['name'] == 'Ada Begg'
        and group['emails'] == 'abegg@example.com'
        for group in results
    )


def test_index_q_emails(client, session):
    session.add_all([
        Group(
            name='Joe Bloggs',
            emails='jbloggs@example.com',
        ),
        Group(
            name='Example, Inc.',
            emails='abegg@example.com;jappleseed@legends.com',
        ),
        Group(
            name='Ada Begg',
            emails='nonspecific@example.com',
        ),
    ])
    session.commit()
    res = client.get('/groups/', json={'q': {'emails': 'abegg'}})
    assert res.status_code == 200
    data = res.get_json()
    assert data['count'] == 1
    group = data['results'][0]
    assert group['name'] == 'Example, Inc.'
    assert group['emails'] == 'abegg@example.com;jappleseed@legends.com'


def test_get(client, session):
    session.add(Group(id=1, name='Joe Bloggs', emails='jbloggs@example.com'))
    session.commit()
    res = client.get('/groups/1')
    assert res.status_code == 200
    data = res.get_json()
    assert data['emails'] == 'jbloggs@example.com'
    assert data['name'] == 'Joe Bloggs'
    assert 'createdAt' in data
    assert 'updatedAt' in data
    assert 'startAt' in data
    assert data['recur'] == 'daily'
    assert data['timeZone'] == 'UTC'
    assert 'createdAt' in data
    assert 'updatedAt' in data


def test_get_nonexistent(client, session):
    nonexistent_id = 2
    assert Group.query.get(nonexistent_id) is None
    res = client.get(f'/groups/{nonexistent_id}')
    assert res.status_code == 404
    assert res.get_json() is None


@mock.patch('dms.groups.routes.logger.info')
def test_create(log_info, client, session):
    res = client.post('/groups/', json={
        'name': 'Joe Bloggs',
        'emails': 'jbloggs@example.com',
    })
    assert res.status_code == 201
    data = res.get_json()
    group = Group.query.get(data['id'])
    assert group.emails == 'jbloggs@example.com'
    assert group.name == 'Joe Bloggs'
    log_info.assert_called_with(
        f"Created new group: <Group {data['id']} \"Joe Bloggs\">")


def test_create_with_recur_monthly(client, session):
    session.commit()
    res = client.post('/groups/', json={
        'name': 'Joe Bloggs',
        'emails': 'jbloggs@example.com',
        'recur': 'monthly',
    })
    assert res.status_code == 201
    data = res.get_json()
    q = Group.query.filter_by(
        id=data['id'],
        name='Joe Bloggs',
        emails='jbloggs@example.com',
        recur='monthly',
    )
    assert q.count() == 1


def test_create_with_time_zone_london(client, session):
    session.commit()
    res = client.post('/groups/', json={
        'name': 'Joe Bloggs',
        'emails': 'jbloggs@example.com',
        'timeZone': 'Europe/London',
    })
    assert res.status_code == 201
    data = res.get_json()
    q = Group.query.filter_by(
        id=data['id'],
        name='Joe Bloggs',
        emails='jbloggs@example.com',
        time_zone='Europe/London',
    )
    assert q.count() == 1


def test_create_with_start_at(client, session):
    session.commit()
    res = client.post('/groups/', json={
        'name': 'Joe Bloggs',
        'emails': 'jbloggs@example.com',
        'startAt': '2020-09-01T12:00:00',
    })
    assert res.status_code == 201
    data = res.get_json()
    q = Group.query.filter_by(
        id=data['id'],
        name='Joe Bloggs',
        emails='jbloggs@example.com',
    )
    assert q.count() == 1
    assert q.first().start_at == datetime.fromisoformat('2020-09-01T12:00:00')


def test_create_no_emails(client, session):
    res = client.post('/groups/', json={'name': 'example'})
    assert res.status_code == 400
    assert Group.query.count() == 0  # assert is still empty


def test_create_no_name(client, session):
    res = client.post('/groups/', json={'emails': 'jbloggs@example.com'})
    assert res.status_code == 400
    assert Group.query.count() == 0  # assert is still empty


@mock.patch('dms.groups.routes.logger.info')
def test_update(log_info, client, session):
    session.add(Group(
        id=1,
        name='John Doe',
        emails='jdoe@example.com'
    ))
    session.commit()
    res = client.put(
        '/groups/1',
        json={
            'name': 'Example, Inc.',
            'emails': 'jdoe@example.com;jappleseed@legends.com',
        }
    )
    assert res.status_code == 200
    group = Group.query.get(1)
    assert group.name == 'Example, Inc.'
    assert group.emails == 'jdoe@example.com;jappleseed@legends.com'
    log_info.assert_called_with(
        'Updated group: <Group 1 "Example, Inc.">')


def test_update_no_emails(client, session):
    session.add(Group(
        id=1,
        name='John Doe',
        emails='jdoe@example.com'
    ))
    session.commit()
    res = client.put('/groups/1', json={'name': 'Example, Inc.'})
    assert res.status_code == 200
    group = Group.query.get(1)
    assert group.name == 'Example, Inc.'
    assert group.emails == 'jdoe@example.com'


def test_update_no_name(client, session):
    session.add(Group(
        id=1,
        name='John Doe',
        emails='jdoe@example.com'
    ))
    session.commit()
    res = client.put(
        '/groups/1',
        json={'emails': 'jdoe@example.com;jappleseed@legends.com'}
    )
    assert res.status_code == 200
    group = Group.query.get(1)
    assert group.name == 'John Doe'
    assert group.emails == 'jdoe@example.com;jappleseed@legends.com'


@mock.patch('dms.groups.routes.logger.info')
def test_delete(log_info, client, session):
    session.add(Group(
        id=1,
        name='John Doe',
        emails='jdoe@example.com'
    ))
    session.commit()
    res = client.delete('/groups/1')
    assert res.status_code == 200
    assert Group.query.get(1) is None
    log_info.assert_called_with(
        'Deleted group: <Group 1 "John Doe">')


def test_delete_nonexistent(client, session):
    session.add(Group(
        id=1,
        name='John Doe',
        emails='jdoe@example.com'
    ))
    session.commit()
    nonexistent_id = 2
    assert Group.query.get(nonexistent_id) is None
    res = client.delete(f'/groups/{nonexistent_id}')
    assert res.status_code == 404
    assert Group.query.count() == 1


TEST_GROUPS_CSV = b"""name,emails
Joe Bloggs,jbloggs@example.com
"Example, Inc.","jdoe@example.com;jappleseed@legends.com"
Ada Begg,abegg@example.com
"""


def test_import_csv(client, session):
    res = client.post(
        '/groups/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={
            'file': (BytesIO(TEST_GROUPS_CSV), 'test_groups.csv')
        }
    )
    assert res.status_code == 200

    def group_exists(name, emails):
        return Group.query.filter_by(name=name, emails=emails).count() == 1

    assert group_exists(
        'Joe Bloggs',
        'jbloggs@example.com')
    assert group_exists(
        'Example, Inc.',
        'jdoe@example.com;jappleseed@legends.com')
    assert group_exists(
        'Ada Begg',
        'abegg@example.com')


def test_import_csv_wrong_extension(client, session):
    res = client.post(
        '/groups/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={
            'file': (BytesIO(TEST_GROUPS_CSV), 'test_groups.txt')
        }
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['message'] == "Invalid file extension"


def test_import_csv_no_file(client, session):
    res = client.post(
        '/groups/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={}
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['message'] == "No file in data"


def test_import_csv_no_filename(client, session):
    res = client.post(
        '/groups/import-csv',
        buffered=True,
        content_type='multipart/form-data',
        data={
            'file': (BytesIO(TEST_GROUPS_CSV), '')
        }
    )
    assert res.status_code == 400
    data = res.get_json()
    assert data['message'] == "No file selected"


def test_job_scheduled_on_model_create(session, scheduler):
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
        start_at=datetime.now() + timedelta(hours=4),
    )
    session.add(group)
    session.commit()

    jobs = scheduler.get_jobs()
    jobs_for_group = [job for job in jobs if job.id == str(group.id)]
    assert len(jobs_for_group) == 1
    job = jobs_for_group[0]
    assert job.next_run_time == group.start_at_with_tz()


def test_job_scheduled_on_model_update(session, scheduler):
    start_time = datetime.now() + timedelta(hours=4)
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
        start_at=start_time,
    )
    session.add(group)
    session.commit()

    group.start_at = start_time + timedelta(hours=1)
    session.add(group)
    session.commit()

    jobs = scheduler.get_jobs()
    jobs_for_group = [job for job in jobs if job.id == str(group.id)]
    assert len(jobs_for_group) == 1
    job = jobs_for_group[0]
    assert job.next_run_time == group.start_at_with_tz()


def test_job_removed_on_model_delete(session, scheduler):
    group = Group(
        name='Joe Bloggs',
        emails='jbloggs@example.com',
        start_at=datetime.now() + timedelta(hours=4),
    )
    session.add(group)
    session.commit()

    jobs = scheduler.get_jobs()
    jobs_for_group = [job for job in jobs if job.id == str(group.id)]
    assert len(jobs_for_group) == 1
    job = jobs_for_group[0]
    assert job.next_run_time == group.start_at_with_tz()

    session.delete(group)
    session.commit()

    jobs = scheduler.get_jobs()
    jobs_for_group = [job for job in jobs if job.id == str(group.id)]
    assert len(jobs_for_group) == 0
