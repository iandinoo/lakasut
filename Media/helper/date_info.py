import datetime
from datetime import timedelta
from pytz import timezone
from dateutil.relativedelta import relativedelta


# %a = weekday(short)

# %A = weekday(full)

# %b = month name(short)

# %B = month name(full)

# %y = year(short)

# %Y = year(full)

# %d = day

# %H = hour(00-23)

# %I = hour(00-12)

# %S = second

# %f = microsecond

# %p = AM/PM

POSTED_COK = datetime.date.today()

time = datetime.datetime.now(timezone("Asia/Jakarta"))

POSTED_DATE = time.strftime("%d-%B-%Y")

POSTED_TIME = time.strftime("%H.%M.%S")

replydate = datetime.datetime.now() + timedelta(days=2)

DATE_OF_REPLY = replydate.strftime("%d-%m-%Y")

CAPTCHA_DATE = datetime.datetime.now() + timedelta(seconds=1)

DATE = POSTED_DATE
TIME = POSTED_TIME
