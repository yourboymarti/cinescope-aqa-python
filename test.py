# # # # class Computer:
# # # #     def power_on(self): print("Computer: powering on")
# # # #     def load_os(self): print("Computer: loading OS")
# # # #
# # # # class IDE:
# # # #     def open(self, project_path: str): print(f"IDE: opening {project_path}")
# # # #
# # # # class Browser:
# # # #     def open(self, url: str): print(f"Browser: opening {url}")
# # # #
# # # # class Messenger:
# # # #     def connect(self): print("Messenger: connecting")
# # # #     def set_status(self, status: str): print(f"Messenger: status -> '{status}'")
# # # #
# # # #
# # # # class WorkdayFacade:
# # # #     def __init__(self):
# # # #         self.computer = Computer()
# # # #         self.ide = IDE()
# # # #         self.browser = Browser()
# # # #         self.messenger = Messenger()
# # # #
# # # #     def start_work_day(self, project_path: str, jira_url: str):
# # # #         self.computer.power_on()
# # # #         self.computer.load_os()
# # # #         self.ide.open(project_path)
# # # #         self.browser.open(jira_url)
# # # #         self.messenger.connect()
# # # #         self.messenger.set_status("online")
# # # #
# # # #
# # # # workday = WorkdayFacade()
# # # # workday.start_work_day("/projects/my-app", "https://jira.company.com")
# # # #
# # # # # После реализации вот это должно вывести все шесть строк по порядку:
# # # # """
# # # # Computer: powering on
# # # # Computer: loading OS
# # # # IDE: opening /projects/my-app
# # # # Browser: opening https://jira.company.com
# # # # Messenger: connecting
# # # # Messenger: status -> online
# # # # """
# # #
# # #
# # #
# # # # def inspect(*args):
# # # #     print(type(args))    # <class 'tuple'>
# # # #     print(args)
# # # #
# # # # inspect("a", "b", "c")  # ('a', 'b', 'c')
# # #
# # # #
# # # # def log(level, *messages, separator=" "):
# # # #     print(f"[{level}] {separator.join(messages)}")
# # # #
# # # # log("INFO", "start", "ok", "done")            # [INFO] start ok done
# # # # log("INFO", "start", "ok", separator=" | ")   # [INFO] start | ok
# # #
# # #
# # #
# # # def print_users(*names):
# # #     for number, name in enumerate(names, start=1):
# # #         print(f"{number}.{name}")
# # #
# # #
# # # print_users("Martin", "Toma")
# # # print_users(a=1, b=2)
# #
# #
# # # def describe_request(**kwargs):
# # #     for key, value in kwargs.items():
# # #         print(f"  {key}: {value}")
# # #
# # # describe_request(method="POST", url="/users", timeout=5)
# # # # method: POST
# # # # url: /users
# # # # timeout: 5
# # #
# # # def inspect(**kwargs):
# # #     print(type(kwargs))  # <class 'dict'>
# # #     print(kwargs)
# # #
# # # inspect(a=1, b=2)   # {'a': 1, 'b': 2}
# #
# #
# # # def create_user(name, role="USER", **kwargs):
# # #     print(f"name={name}, role={role}")
# # #     print(f"extra: {kwargs}")
# # #
# # # create_user("Alice", role="ADMIN", email="a@test.com", active=True)
# # # # name=Alice, role=ADMIN
# # # # extra: {'email': 'a@test.com', 'active': True}
# #
# #
# # #
# # # def build_headers(**kwargs):
# # #     return kwargs
# # #
# # # # print(build_headers(content_type="application/json", authorization="Bearer token123")
# # # # print(build_headers("application/json"))
# # #
# # # def send(method, *endpoints, timeout=30, **extra):
# # #     print(f"method={method}")
# # #     print(f"endpoints={endpoints}")
# # #     print(f"timeout={timeout}")
# # #     print(f"extra={extra}")
# # #
# # # send("GET", "/users", "/posts", timeout=10, verify=False)
# # # # method=GET
# # # # endpoints=('/users', '/posts')
# # # # timeout=10
# # # # extra={'verify': False}
# #
# # #
# # # def broken(**kwargs, *args):
# # #     pass
# #
# #
# # def wrapper(*args, **kwargs):
# #     print("до вызова")
# #     result = target(args, kwargs)
# #     print("после вызова")
# #     return result
# #
# # def target(method, url, timeout=30):
# #     print(f"{method} {url} (timeout={timeout})")
# #
# # wrapper("GET", "/users", timeout=5)
# # # до вызова
# # # GET /users (timeout=5)
# # # после вызова
#
#
#
# # import pytest
# #
# #
# # @pytest.mark.parametrize("input_data,expected", [(1, 2), (2, 4), (3, 6)])
# # def test_multiply_by_two(input_data, expected):
# #     assert input_data * 2 == expected
#
# # import pytest
# #
# #
# # @pytest.mark.parametrize("parameter_name", ["value1", "value2"])
# # class TestParametrizedClass:
# #     def test_first(self, parameter_name):
# #         print(f"Тест 1 прогон: {parameter_name}")
# #         assert True
# #
# #     def test_second(self, parameter_name):
# #         print(f"Тест 2 прогон: {parameter_name}")
# #         assert True
#
#
# # import pytest
# #
# #
# # @pytest.mark.parametrize("param_a,param_b", [
# #     ("a1", "b1"),
# #     ("a2", "b2")
# # ])
# # class TestMultipleParams:
# #
# #     def test_params_combination(self, param_a, param_b):
# #         print(f"1 тест: {param_a} и {param_b}")
# #
# #     def test_another_method(self, param_a, param_b):
# #         combined = f"{param_a}-{param_b}"
# #         print(f"2 тест: {combined}")
# #         assert len(combined) > 2
#
#
# import pytest
#
#
# @pytest.mark.parametrize("class_param", ["c1", "c2"])
# class TestCombinedParametrization:
#
#     @pytest.mark.parametrize("method_param", ["m1", "m2", "m3"])
#     def test_combination(self, class_param, method_param):
#         # Этот тест запустится 6 раз (2 параметра класса × 3 параметра метода)
#         print(f"Тест 1 с параметризацией класса={class_param} и метода={method_param}")
#         assert True
#
#     def test_only_class_param(self, class_param):
#         # Этот тест запустится 2 раза (только с параметрами класса)
#         print(f"Тест 2 с параметризацией только класса={class_param}")
#         assert True
#


# import pytest
#
#
# @pytest.mark.parametrize("feature_flag,platform", [
#     ("feature_a", "windows"),
#     ("feature_a", "mac"),
#     ("feature_b", "windows"),
#     pytest.param("feature_b", "mac", marks=pytest.mark.skip(reason="Not supported on Mac"))
# ])
# class TestFeatures:
#
#     def test_feature_availability(self, feature_flag, platform):
#         print(f"Testing {feature_flag} on {platform}")
#         assert True
#

