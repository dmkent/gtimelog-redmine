"""Wrapper to easily add time to Redmine tickets."""
from redmine import Redmine


class RedmineConnection(object):
    """Class to simpify connection to Redmine."""
    def __init__(self, host, **kwargs):
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

if __name__ =='__main__':
    conn = RedmineConnection('http://localhost/redmine', key=u'd4c5d80600fb6f61753e8b6650098b151617acdf', version=1.3)

    conn.log_time(1, 0.5, comments=u'from me in api')

