from config import REPORT_FILE, TIME_FORMAT


class SessionReport:
    @staticmethod
    def write(user):
        time_in = user.time_in.strftime(TIME_FORMAT)
        time_out = user.time_out.strftime(TIME_FORMAT)
        login_width = max(8, len(user.login))

        border = "+" + "-" * (login_width + 2) + "+" + "-" * 21 + "+" + "-" * 21 + "+"
        separator = "|" + "-" * (login_width + 2) + "|" + "-" * 21 + "|" + "-" * 21 + "|"
        header = f"| {'login':<{login_width}} | {'time_in':<19} | {'time_out':<19} |"
        row = f"| {user.login:<{login_width}} | {time_in} | {time_out} |"
        table = "\n".join((border, header, separator, row, border, ""))

        with open(REPORT_FILE, "a", encoding="utf-8") as file:
            file.write(table + "\n")
