import json
import logging

import pika
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.event import listens_for

from dms.config import RABBITMQ_HOST, RABBITMQ_QUEUE

from .models import Group

logger = logging.Logger(__name__)

scheduler = BackgroundScheduler()


def start_scheduler(db_url):
    jobstore = SQLAlchemyJobStore(url=db_url)
    scheduler.add_jobstore(jobstore, alias='default')
    scheduler.start()


def _publish_scan_job(group):
    params = pika.ConnectionParameters(host=RABBITMQ_HOST, heartbeat=0)
    try:
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(RABBITMQ_QUEUE)
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(group.serialize()),
        )
    finally:
        connection.close()


def _trigger(group):
    t = group.start_at_with_tz()
    trigger_params = {
        'start_date': t,
        'hour': t.hour,
        'minute': t.minute,
        'second': t.second,
        'timezone': group.tz(),
    }
    if group.recur == 'weekly':
        trigger_params['day_of_week'] = t.day_of_week,
    if group.recur == 'monthly':
        # TODO: figure out how to handle day of month
        trigger_params['day'] = 1
    return CronTrigger(**trigger_params)


def _schedule_scan_job(group):
    scheduler.add_job(
        _publish_scan_job,
        trigger=_trigger(group),
        id=str(group.id),
        replace_existing=True,
        args=[group],
    )


def _remove_scan_job(group):
    scheduler.remove_job(str(group.id))


@listens_for(Group, 'after_insert')
def _on_group_created(mapper, connection, target):
    _schedule_scan_job(target)


@listens_for(Group, 'after_update')
def _on_group_updated(mapper, connection, target):
    _schedule_scan_job(target)


@listens_for(Group, 'after_delete')
def _on_group_removed(mapper, connection, target):
    _remove_scan_job(target)
