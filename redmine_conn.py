"""Wrapper to easily add time to Redmine tickets."""
from redmine import Redmine


class RedmineConnection(object):
    """Class to simpify connection to Redmine."""
    def __init__(self, **kwargs):
        if 'host' not in kwargs:
            raise ValueError('No redmine host specified.')

        host = kwargs.pop('host')
        self._redmine = Redmine(host, **kwargs)

        self._activity_id = 9

    def log_time(self, issue_id, hours, **kwargs):
        """Log some time to a ticket."""
        try:
            issue = self._redmine.issues.get(issue_id)
        except:
            raise ValueError('Unable to find issue %d' % issue_id)

        issue.time_entries.new(hours=hours,
                               activity_id=self._activity_id,
                               **kwargs)
