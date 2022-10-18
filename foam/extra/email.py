__all__ = ['Envelope', 'SMTP']


import pathlib as p
import time
import typing as t

from ..base.type import Path

if t.TYPE_CHECKING:
    from email.message import EmailMessage

    from typing_extensions import Self


class Envelope:
    '''
    Reference:
        - https://github.com/tomekwojcik/envelopes
    '''

    def __init__(self, *to_addresses: str) -> None:
        self._header = {'To': ', '.join(to_addresses)}
        self._applies = []

    @classmethod
    def to(cls, *addresses: str) -> 'Self':
        return cls(*addresses)

    def add_attachment(self, path: Path, type: t.Optional[str] = None, **kwargs: t.Any) -> 'Self':
        '''
        Reference:
            - https://docs.python.org/zh-cn/3/library/email.examples.html
        '''
        path = p.Path(path)
        if type is None:
            import mimetypes

            type, encoding = mimetypes.guess_type(path.as_posix(), strict=True)
            if type is None or encoding is not None:
                type = 'application/octet-stream'
        maintype, subtype = type.split('/', maxsplit=1)
        content = path.read_bytes()
        kwargs = {'maintype': maintype, 'subtype': subtype, 'filename': path.name, **kwargs}
        self._applies.append(lambda msg: msg.add_attachment(content, **kwargs))
        return self

    def set(self, **kwargs: str) -> 'Self':
        for key, value in kwargs.items():
            getattr(self, f'set_{key}')(value)
        return self

    def set_date(self, timestamp: t.Optional[float]) -> 'Self':
        from email.utils import formatdate

        self._header['Date'] = formatdate(timestamp, localtime=True, usegmt=False)

    def set_content(self, value: str, html: bool = False) -> 'Self':
        self._applies.append(lambda msg: msg.set_content(value, subtype='html' if html else 'plain'))
        return self

    def set_content_by_path(self, value: Path, html: bool = False) -> 'Self':
        return self.set_content(p.Path(value).read_text(), html)

    def set_subject(self, value: str) -> 'Self':
        self._header['Subject'] = value
        return self

    def to_message(self) -> 'EmailMessage':
        from email.message import EmailMessage

        msg = EmailMessage()
        # _header
        for key, value in self._header.items():
            msg[key] = value
        # _applies
        for apply in self._applies:
            apply(msg)
        return msg

    def send_by(self, *smtps: 'SMTP') -> 'Self':
        for smtp in smtps:
            smtp.send(self)
        return self


class SMTP:
    '''SMTP wrapper

    Example:
        >>> with SMTP['163'](ssl=False).login(username, password) as smtp:
        ...     Envelope \
        ...         .to('liangiydon@gmail.com') \
        ...         .set_subject('SMTP Test') \
        ...         .set_content('Here is the <a href="http://www.python.org">link</a> you wanted.', html=True) \
        ...         .add_attachment(__file__) \
        ...         .send_by(smtp)
    '''

    def __init__(self, domain: str, host: str, port: int, ssl: bool = True) -> None:
        import smtplib

        self._domain = domain
        self._smtp = (smtplib.SMTP_SSL if ssl else smtplib.SMTP)(host, port)
        self._username = None

    def __enter__(self) -> 'Self':
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.quit()

    def __class_getitem__(cls, key: str) -> 'Self':
        return {
            '163': lambda ssl: cls('163.com', 'smtp.163.com', 25, ssl),  # mail.163.com
        }[key]

    @property
    def sender(self) -> str:
        assert self._username is not None, 'Please login first'
        return f'{self._username}@{self._domain}'

    def login(self, username: str, password: str) -> 'Self':
        self._username = username
        self._smtp.login(username, password)
        return self

    def quit(self) -> None:
        # NOTE: Lifetime of this instance ends after quit is called, so it will not return self
        self._smtp.__exit__()

    def send(self, *envelopes: 'Envelope') -> 'Self':
        for envelope in envelopes:
            msg = envelope.to_message()
            msg['From'] = self.sender
            self._smtp.send_message(msg)
        return self

    def wait(self, seconds: float) -> 'Self':
        time.sleep(seconds)
        return self
