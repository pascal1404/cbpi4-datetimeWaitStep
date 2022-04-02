# -*- coding: utf-8 -*-
import os
import asyncio
from aiohttp import web
from cbpi.api import parameters, Property, action
from cbpi.api.step import StepResult, CBPiStep
from cbpi.api.timer import Timer
from datetime import datetime
import time
from voluptuous.schema_builder import message
from cbpi.api.dataclasses import NotificationAction, NotificationType
from cbpi.api.dataclasses import Kettle, Props
from cbpi.api import *
import logging

logger = logging.getLogger(__name__)

@parameters([Property.Text(label="Datetime",configurable = True, description = "datestring that represent time to MashIn. Format(dd.mm.yy-HH:MM)"),])
class DatetimeWaitStep(CBPiStep):

    async def on_timer_done(self, timer):
        self.summary = ""
        self.cbpi.notify(self.name, 'datetime reached. Starting next step', NotificationType.SUCCESS)
        await self.next()

    async def on_timer_update(self, timer, seconds):
        self.summary = Timer.format_time(seconds)
        await self.push_update()

    async def on_start(self):
        target_datetime = datetime.strptime(self.props.get("Datetime", datetime.now()), '%d.%m.%y-%H:%M')
        now = datetime.now()
        seconds = (target_datetime - now).total_seconds()
        self.timer = Timer(int(seconds), on_update=self.on_timer_update, on_done=self.on_timer_done)
        self.timer.start()

    async def on_stop(self):
        await self.timer.stop()
        self.summary = ""
        await self.push_update()

    async def reset(self):
        target_datetime = datetime.strptime(self.props.get("Datetime", datetime.now()), '%d.%m.%y-%H:%M')
        now = datetime.now()
        seconds = (target_datetime - now).total_seconds()
        self.timer = Timer(int(seconds), on_update=self.on_timer_update, on_done=self.on_timer_done)

    async def run(self):
        while self.running == True:
            await asyncio.sleep(1)
        return StepResult.DONE

def setup(cbpi):
    cbpi.plugin.register("DatetimeWaitStep", DatetimeWaitStep)
    pass
