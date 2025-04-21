from datetime import datetime
import pytz


def generate_timestamp(self) -> str:
        """Generates a timestamp."""

        tz = pytz.timezone("America/Argentina/Buenos_Aires")
        current_date = datetime.now(tz=tz)
        current_date = current_date.strftime('%y%m%d')

        timestamp = str(datetime.now().strftime("%H%M%S.%f").replace(".", ""))
        timestamp = current_date + timestamp[:8]
        return timestamp