from config import REPORT_FILE, TIME_FORMAT


class SessionReport:
    # При каждом закрытии добавляем одну строку с временем работы пользователя.
    @staticmethod
    def write(user):
        time_in = user.time_in.strftime(TIME_FORMAT)
        time_out = user.time_out.strftime(TIME_FORMAT)
        width = max(8, len(user.login))
        border = "+" + "-" * (width + 2) + "+" + "-" * 21 + "+" + "-" * 21 + "+"
        header = ("| " + "login".ljust(width) + " | " + "time_in".ljust(19)
                  + " | " + "time_out".ljust(19) + " |")
        row = ("| " + user.login.ljust(width) + " | " + time_in
               + " | " + time_out + " |")
        separator = ("|" + "-" * (width + 2) + "|" + "-" * 21
                     + "|" + "-" * 21 + "|")
        with open(REPORT_FILE, "a", encoding="utf-8") as file:
            file.write(border + "\n" + header + "\n" + separator + "\n"
                       + row + "\n" + border + "\n\n")
