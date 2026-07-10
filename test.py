# # class Computer:
# #     def power_on(self): print("Computer: powering on")
# #     def load_os(self): print("Computer: loading OS")
# #
# # class IDE:
# #     def open(self, project_path: str): print(f"IDE: opening {project_path}")
# #
# # class Browser:
# #     def open(self, url: str): print(f"Browser: opening {url}")
# #
# # class Messenger:
# #     def connect(self): print("Messenger: connecting")
# #     def set_status(self, status: str): print(f"Messenger: status -> '{status}'")
# #
# #
# # class WorkdayFacade:
# #     def __init__(self):
# #         self.computer = Computer()
# #         self.ide = IDE()
# #         self.browser = Browser()
# #         self.messenger = Messenger()
# #
# #     def start_work_day(self, project_path: str, jira_url: str):
# #         self.computer.power_on()
# #         self.computer.load_os()
# #         self.ide.open(project_path)
# #         self.browser.open(jira_url)
# #         self.messenger.connect()
# #         self.messenger.set_status("online")
# #
# #
# # workday = WorkdayFacade()
# # workday.start_work_day("/projects/my-app", "https://jira.company.com")
# #
# # # После реализации вот это должно вывести все шесть строк по порядку:
# # """
# # Computer: powering on
# # Computer: loading OS
# # IDE: opening /projects/my-app
# # Browser: opening https://jira.company.com
# # Messenger: connecting
# # Messenger: status -> online
# # """
#
#
#
# # def inspect(*args):
# #     print(type(args))    # <class 'tuple'>
# #     print(args)
# #
# # inspect("a", "b", "c")  # ('a', 'b', 'c')
#
# #
# # def log(level, *messages, separator=" "):
# #     print(f"[{level}] {separator.join(messages)}")
# #
# # log("INFO", "start", "ok", "done")            # [INFO] start ok done
# # log("INFO", "start", "ok", separator=" | ")   # [INFO] start | ok
#
#
#
# def print_users(*names):
#     for number, name in enumerate(names, start=1):
#         print(f"{number}.{name}")
#
#
# print_users("Martin", "Toma")
# print_users(a=1, b=2)


# def describe_request(**kwargs):
#     for key, value in kwargs.items():
#         print(f"  {key}: {value}")
#
# describe_request(method="POST", url="/users", timeout=5)
# # method: POST
# # url: /users
# # timeout: 5
#
# def inspect(**kwargs):
#     print(type(kwargs))  # <class 'dict'>
#     print(kwargs)
#
# inspect(a=1, b=2)   # {'a': 1, 'b': 2}


# def create_user(name, role="USER", **kwargs):
#     print(f"name={name}, role={role}")
#     print(f"extra: {kwargs}")
#
# create_user("Alice", role="ADMIN", email="a@test.com", active=True)
# # name=Alice, role=ADMIN
# # extra: {'email': 'a@test.com', 'active': True}


#
# def build_headers(**kwargs):
#     return kwargs
#
# # print(build_headers(content_type="application/json", authorization="Bearer token123")
# # print(build_headers("application/json"))
#
# def send(method, *endpoints, timeout=30, **extra):
#     print(f"method={method}")
#     print(f"endpoints={endpoints}")
#     print(f"timeout={timeout}")
#     print(f"extra={extra}")
#
# send("GET", "/users", "/posts", timeout=10, verify=False)
# # method=GET
# # endpoints=('/users', '/posts')
# # timeout=10
# # extra={'verify': False}

#
# def broken(**kwargs, *args):
#     pass


def wrapper(*args, **kwargs):
    print("до вызова")
    result = target(args, kwargs)
    print("после вызова")
    return result

def target(method, url, timeout=30):
    print(f"{method} {url} (timeout={timeout})")

wrapper("GET", "/users", timeout=5)
# до вызова
# GET /users (timeout=5)
# после вызова