from singleton_decorator import singleton
import re
from Cardinal import Cardinal

@singleton
class Time:
    """
    Steps:
    - 1 Strip the token to remove extra spaces
    - 2 Try to match "hh:mm"
      - 2.1 Add the hour
      - 2.2 Add the minute if it exists and is not 00
    - 3 Otherwise, try to match "(hh:)mm:ss(.ms)"
      - 3.1 If hour, add it as cardinal and add "time" with proper plurality
      - 3.2 If minute, add it as cardinal and add "minutt" with proper plurality
      - 3.3 If seconds, add "og" if seconds is the last number, add seconds as cardinal, and "sekund" with proper plurality
      - 3.4 If milliseconds, add "og", milliseconds as cardinal, and "millisekund" with proper plurality
    - 4 Handle special cases like "kvart på" and "halv"

    Edge case:
    "PM2" -> "to p m"
    """
    def __init__(self):
        super().__init__()

        # Regex to filter out dots
        self.filter_regex = re.compile(r"[. ]")
        # Regex to detect time in the form hh:mm
        self.time_regex = re.compile(r"^(?P<hour>\d{2}):(?P<minute>\d{2})$")
        # Regex to detect time in the form hh:mm:ss
        self.full_time_regex = re.compile(r"^(?:(?P<hour>\d{2}):)?(?P<minute>\d{2})(?::(?P<seconds>\d{2})(?:\.(?P<milliseconds>\d{2}))?)?$")
        # Cardinal conversion
        self.cardinal = Cardinal()

    def convert(self, token: str) -> str:
        # 1 Strip the token to remove extra spaces
        token = token.strip()

        result_list = []

        # 2 Try to match "hh:mm"
        match = self.time_regex.match(token)
        if match:
            # Extract hour and minute from the match
            hour, minute = match.group("hour"), match.group("minute")
            hour, minute = int(hour), int(minute)
            if hour < 10:
                result_list.append("null")
            result_list.append(self.cardinal.convert(str(hour)))

            # 2.2 Add the minute if it exists and is not just zeros
            if minute < 10:
                result_list.append("null")
            result_list.append(self.cardinal.convert(str(minute)))

            return " ".join(result_list)

        # 3 Try to match "(hh:)mm:ss(.ms)"
        match = self.full_time_regex.match(token)
        if match:
            # Extract values from match
            hour, minute, seconds, milliseconds = match.group("hour"), match.group("minute"), match.group("seconds"), match.group("milliseconds")
            hour = int(hour) if hour else None
            minute = int(minute)
            seconds = int(seconds) if seconds else None
            milliseconds = int(milliseconds) if milliseconds else None

            # 3.1 If hour, add it as cardinal and add "time" with proper plurality
            if hour is not None:
                if hour < 10:
                    result_list.append("null")
                result_list.append(self.cardinal.convert(str(hour)))
                result_list.append("time" if hour == 1 else "timer")
            # 3.2 If minute, add it as cardinal and add "minutt" with proper plurality
            if minute:
                if minute < 10:
                    result_list.append("null")
                result_list.append(self.cardinal.convert(str(minute)))
                result_list.append("minutt" if minute == 1 else "minutter")
            # 3.3 If seconds, add "og" if seconds is the last number, add seconds as cardinal, and "sekund" with proper plurality
            if seconds:
                if not milliseconds:
                    result_list.append("og")
                result_list.append(self.cardinal.convert(str(seconds)))
                result_list.append("sekund" if seconds == 1 else "sekunder")
            # 3.4 If milliseconds, add "og", milliseconds as cardinal, and "millisekund" with proper plurality
            if milliseconds:
                result_list.append("og")
                result_list.append(self.cardinal.convert(str(milliseconds)))
                result_list.append("millisekund" if milliseconds == 1 else "millisekunder")

            return " ".join(result_list)

        # Return the original token if no match was found
        return token
