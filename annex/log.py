from datetime import datetime
import re
import uuid

from schematics.models import Model
from schematics.types import StringType, DecimalType, DateTimeType, UUIDType


class Annex(Model):
    id = UUIDType(required=True)
    timestamp = DateTimeType(required=True, serialized_format='%s.%f')
    desc = StringType(required=True)


class UUIDLog(object):
    def __init__(self):
        pass

    def parselog(self, logfile):
        annexes = []
	with open(logfile, 'r') as fp:
            for line in fp:
	        a = Annex()
                a.id, a.desc, a.timestamp = self.parseline(line.strip())
		try:
                    a.validate()
                    annexes.append(a)
                except ModelValidationError:
                    pass
	return annexes

    def parseline(self, line):
        pattern = '(?P<uuid>[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}) (?P<desc>.*) timestamp=(?P<timestamp>\d+.\d+)s$'
        s = re.match(pattern, line)

        return (
            uuid.UUID(s.group('uuid')), s.group('desc'),
            datetime.fromtimestamp(float(s.group('timestamp'))))
