__all__ = ['Envelope', 'SMTP']


import email.message
import email.utils
import mimetypes
import pathlib as p
import smtplib
import time
import typing as t

from ..implementation import Base
from ...base.type import Any, Func1, Path

if t.TYPE_CHECKING:
    import typing_extensions as te

    P = te.ParamSpec('P')
    Kwargs = te.ParamSpecKwargs(P)


class Envelope(Base):
    '''Envelope

    Reference:
        - https://github.com/tomekwojcik/envelopes
    '''

    __slots__ = ('_header', '_applies')
    _smtp = None

    def __init__(self, *to_addresses: str) -> None:
        self._header = {'To': ', '.join(to_addresses)}
        self._applies: t.List[Func1[email.message.EmailMessage, None]] \
            = [lambda msg: None]

    @classmethod
    def auto(cls, smtp: 'SMTP') -> type:
        '''Auto-delivered envelope'''
        cls._smtp = smtp
        return cls

    @classmethod
    def to(cls, *addresses: str) -> 'te.Self':
        return cls(*addresses)

    def add_attachment(self, path: Path, type: t.Optional[str] = None, **kwargs: 'Kwargs') -> 'te.Self':
        '''
        Reference:
            - https://docs.python.org/zh-cn/3/library/email.examples.html
        '''
        path = p.Path(path)
        if type is None:
            type, encoding = mimetypes.guess_type(path.as_posix(), strict=True)
            if type is None or encoding is not None:
                type = 'application/octet-stream'
        maintype, subtype = type.split('/', maxsplit=1)
        content = path.read_bytes()
        kwargs = {'maintype': maintype, 'subtype': subtype, 'filename': path.name, **kwargs}
        self._applies.append(lambda msg: msg.add_attachment(content, **kwargs))
        return self

    def set(self, **kwargs: str) -> 'te.Self':
        for key, value in kwargs.items():
            getattr(self, f'set_{key}')(value)
        return self

    def set_date(self, value: t.Optional[float]) -> 'te.Self':
        self._header['Date'] = email.utils.formatdate(value, localtime=True, usegmt=False)
        return self

    def set_content(self, value: str, html: bool = False) -> 'te.Self':
        apply: Func1[email.message.EmailMessage, None] \
            = lambda msg: msg.set_content(value, subtype='html' if html else 'plain')
        self._applies[0] = apply
        return self

    def set_content_by_path(self, value: Path, html: bool = False) -> 'te.Self':
        return self.set_content(p.Path(value).read_text(), html)

    def set_html(self, value: str) -> 'te.Self':
        return self.set_content(value, html=True)

    def set_html_by_path(self, value: Path) -> 'te.Self':
        return self.set_content_by_path(value, html=True)

    def set_text(self, value: str) -> 'te.Self':
        return self.set_content(value, html=False)

    def set_text_by_path(self, value: Path) -> 'te.Self':
        return self.set_content_by_path(value, html=False)

    def set_subject(self, value: str) -> 'te.Self':
        self._header['Subject'] = value
        return self

    def to_message(self) -> email.message.EmailMessage:
        msg = email.message.EmailMessage()
        # _header
        for key, value in self._header.items():
            msg[key] = value
        # _applies
        for apply in self._applies:
            apply(msg)
        return msg

    def send_by(self, *smtps: 'SMTP') -> 'te.Self':
        for smtp in smtps:
            smtp.send(self)
        return self

    def send(self) -> None:
        assert self._smtp is not None, 'Please do not use this class directly'

        self.send_by(self._smtp)


class SMTP(Base):
    '''SMTP wrapper

    Example:
        >>> with SMTP.aio('163', username, password, ssl=False) as smtp:
        ...     smtp.envelope \\
        ...         .to('liangiydon@gmail.com') \\
        ...         .set_subject('SMTP Test') \\
        ...         .set_content('Here is the <a href="http://www.python.org">link</a> you wanted.', html=True) \\
        ...         .add_attachment(__file__) \\
        ...         .send()
    '''

    __slots__ = ('_domain', '_smtp', '_username')

    def __init__(self, domain: str, host: str, port: int, ssl: bool = True) -> None:
        self._domain = domain
        self._smtp = (smtplib.SMTP_SSL if ssl else smtplib.SMTP)(host, port)
        self._username = None

    def __enter__(self) -> 'te.Self':
        return self

    def __exit__(self, type: Any, value: Any, traceback: Any) -> None:
        self._smtp.__exit__(type, value, traceback)

    def __class_getitem__(cls, key: str) -> 'te.Self':
        # TODO: look forward to adding more
        return {
            '163': lambda ssl: cls('163.com', 'smtp.163.com', 25, ssl),  # mail.163.com
            'qq': lambda ssl: cls('qq.com', 'smtp.qq.com', 587, ssl),  # mail.qq.com
        }[key]

    @classmethod
    def aio(cls, mail: str, username: str, password: str, ssl: bool = True) -> 'te.Self':
        '''All-in-one'''
        return cls[mail](ssl).login(username, password)

    @property
    def sender(self) -> str:
        assert self._username is not None, 'Please login first'

        return f'{self._username}@{self._domain}'

    @property
    def envelope(self) -> 'Envelope':
        return Envelope.auto(self)

    def login(self, username: str, password: str) -> 'te.Self':
        self._username = username
        self._smtp.login(username, password)
        return self

    def quit(self) -> None:
        # NOTE: lifetime of this instance ends after quit is called, so it will not return self
        try:
            self._smtp.quit()
        except smtplib.SMTPServerDisconnected:
            pass

    def send(self, *envelopes: 'Envelope') -> 'te.Self':
        for envelope in envelopes:
            msg = envelope.to_message()
            msg['From'] = self.sender
            self._smtp.send_message(msg)
        return self

    def wait(self, seconds: float) -> 'te.Self':
        time.sleep(seconds)
        return self
