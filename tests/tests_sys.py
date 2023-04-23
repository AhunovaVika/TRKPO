from time import sleep
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase, TransactionTestCase, TestCase, Client, override_settings, tag
from selenium.webdriver.common.by import By


#
#   Default creds
#   systest - 1337Tests
#   systest2 - 1337Tests2
#
#
@tag('selenium')
@override_settings(ALLOWED_HOSTS=['*'])
class BaseTestCase(LiveServerTestCase):
    host = '0.0.0.0'
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set host to externally accessible web server address
        cls.host = socket.gethostbyname(socket.gethostname())

        # Instantiate the remote WebDriver
        cls.selenium = webdriver.Remote(
            #  Set to: htttp://{selenium-container-name}:port/wd/hub
            #  In our example, the container is named `selenium`
            #  and runs on port 4444
            command_executor='http://selenium:4444/wd/hub',
            # Set to CHROME since we are using the Chrome container
            desired_capabilities=DesiredCapabilities.CHROME,

        )
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class SysTests(BaseTestCase):

    def test_010_Index(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element(by=By.XPATH, value='/html/body/nav/div/ul[2]/li[2]/a').get_attribute(
            'href')
        self.assertEquals(signup_navlink, self.live_server_url + '/accounts/signup/')

    def test_020_Signup(self):
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)

        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        login_page_header = driver.find_element_by_xpath('/html/body/h2').text
        self.assertEquals(login_page_header, 'Login')

    def test_030_Signin(self):
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)

        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        # signin
        # driver = self.selenium
        # driver.get(self.live_server_url)
        # signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        # driver.get(signin_navlink)

        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()

        user_link_on_homepage = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        self.assertEquals(user_link_on_homepage,
                          self.live_server_url + '/accounts/p/systest/')  # http://127.0.0.1:8000/accounts/p/systest/

    def test_040_Signout(self):
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)

        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        # signin

        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()

        # signout
        user_link_on_homepage = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        self.assertEquals(user_link_on_homepage,
                          self.live_server_url + '/accounts/p/systest/')  # http://127.0.0.1:8000/accounts/p/systest/

        logout_button = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a')
        logout_button.click()

        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        self.assertEquals(signup_navlink, self.live_server_url + '/accounts/signup/')

    def test_050_Create_table(self):
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)

        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()

        # 1 Log in
        driver = self.selenium
        driver.get(self.live_server_url)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)

        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()

        # 2 Create table
        create_table_button = driver.find_element_by_xpath('/html/body/a[2]')
        create_table_button.click()

        table_name_textbox = driver.find_element_by_xpath('//*[@id="id_name"]')
        buy_in_textbox = driver.find_element_by_xpath('//*[@id="id_buyIn"]')
        max_players_textbox = driver.find_element_by_xpath('//*[@id="id_maxNoOfPlayers"]')
        create_button = driver.find_element_by_xpath('/html/body/form/button')

        table_name_textbox.send_keys('Test table 1')
        buy_in_textbox.send_keys(300)
        max_players_textbox.send_keys(3)
        create_button.click()

        # 5 Exit
        sleep(2)
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()

        # 3 Getting proofs
        driver.get(self.live_server_url)
        homepage_test_table = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/h5').text
        self.assertEquals(homepage_test_table, 'Test table 1')

    def test_060_Join_table(self):
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)

        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        # 1 Log in
        driver = self.selenium
        driver.get(self.live_server_url)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)

        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()

        # 2 Joining game
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 3 Getting proofs
        chat_header = driver.find_element_by_xpath('/html/body/div/div/div[2]/h3').text
        self.assertEquals(chat_header, 'Chat')
        sleep(2)

        # 5 Exit
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()

    def test_070_Leave_table(self):
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)

        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        # 1 Log in
        driver = self.selenium
        driver.get(self.live_server_url)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)

        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()

        # 2 Joining game
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()
        sleep(2)

        chat_header = driver.find_element_by_xpath('/html/body/div/div/div[2]/h3').text
        self.assertEquals(chat_header, 'Chat')

        # 3 Leaving game
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()

        # 4 Getting proofs
        homepage_test_table = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/h5').text
        self.assertEquals(homepage_test_table, 'Test table 1')

    def test_080_Chat(self):
        driver2 = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)
        sleep(1)
        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')
        sleep(1)
        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        sleep(1)
        driver.get(self.live_server_url)
        sleep(1)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()
        sleep(1)
        # 0 Registration of second user
        driver2.get(self.live_server_url)
        signup_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver2.get(signup_navlink)
        sleep(1)
        username_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver2.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver2.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver2.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest2')
        email_textbox.send_keys('systest2@acme.com')
        password1_textbox.send_keys('1337Tests2')
        password2_textbox.send_keys('1337Tests2')
        signup_button.click()
        sleep(1)
        # 1.1 Login
        driver2.get(self.live_server_url)
        signin_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver2.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver2.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest2')
        password_login_textbox.send_keys('1337Tests2')
        login_button.click()
        sleep(1)
        
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 2.1 Joining table
        join_game_button = driver2.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()
        sleep(2)
        # 3 Texting to chat
        chat_textbox = driver.find_element_by_xpath('//*[@id="chat-message-input"]')
        chat_textbox.send_keys('Hello World!')
        chat_textbox.send_keys(Keys.ENTER)
        sleep(1)

        # 4 Getting proofs
        chat = driver2.find_element_by_xpath('//*[@id="chat-log"]').get_attribute('value')
        self.assertEquals(chat, 'systest: Hello World!')

        # 5 Exit
        driver.switch_to.window("systest")
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()
        sleep(1)
        driver2.switch_to.window("systest2")
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()
        driver2.quit()
        
    def test_090_Fold(self):
        driver2 = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)
        sleep(1)
        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')
        sleep(1)
        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        sleep(1)
        driver.get(self.live_server_url)
        sleep(1)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()
        sleep(1)
        # 0 Registration of second user
        driver2.get(self.live_server_url)
        signup_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver2.get(signup_navlink)
        sleep(1)
        username_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver2.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver2.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver2.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest2')
        email_textbox.send_keys('systest2@acme.com')
        password1_textbox.send_keys('1337Tests2')
        password2_textbox.send_keys('1337Tests2')
        signup_button.click()
        sleep(1)
        # 1.1 Login
        driver2.get(self.live_server_url)
        signin_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver2.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver2.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest2')
        password_login_textbox.send_keys('1337Tests2')
        login_button.click()
        sleep(1)

        # 2 Joining table
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 2.1 Joining table
        join_game_button = driver2.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()
        sleep(2)

        # 3 Folding
        fold_button = driver.find_element_by_xpath('//*[@id="fold"]')
        fold_button.click()

        # 4 Getting proofs
        money = driver2.find_element_by_xpath('//*[@id="money-in-table"]').text
        self.assertEquals(money, 'Money: 294')
        sleep(2)

        # 5 Exit
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()
        sleep(2)

        exit_game_button = driver2.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()

    def test_100_Dealer_change(self):
        driver2 = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)
        sleep(1)
        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')
        sleep(1)
        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        sleep(1)
        driver.get(self.live_server_url)
        sleep(1)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()
        sleep(1)
        # 0 Registration of second user
        driver2.get(self.live_server_url)
        signup_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver2.get(signup_navlink)
        sleep(1)
        username_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver2.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver2.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver2.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest2')
        email_textbox.send_keys('systest2@acme.com')
        password1_textbox.send_keys('1337Tests2')
        password2_textbox.send_keys('1337Tests2')
        signup_button.click()
        sleep(1)
        # 1.1 Login
        driver2.get(self.live_server_url)
        signin_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver2.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver2.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest2')
        password_login_textbox.send_keys('1337Tests2')
        login_button.click()
        sleep(1)

        # 2 Joining table
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 2.1 Joining table
        join_game_button = driver2.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()
        sleep(2)

        # 3 Getting dealer
        first_dealer = driver.find_element_by_xpath('//*[@id="dealer"]').text
        self.assertEquals(first_dealer, 'Dealer: systest')

        # 3.1 Folding
        fold_button = driver.find_element_by_xpath('//*[@id="fold"]')
        fold_button.click()
        sleep(2)

        # 4 Getting proofs
        second_dealer = driver.find_element_by_xpath('//*[@id="dealer"]').text
        self.assertEquals(second_dealer, 'Dealer: systest2')
        sleep(2)

        # 5 Exit
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()
        sleep(2)

        exit_game_button = driver2.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()

    def test_110_Game_start(self):
        driver2 = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)
        sleep(1)
        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')
        sleep(1)
        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        sleep(1)
        driver.get(self.live_server_url)
        sleep(1)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()
        sleep(1)
        # 0 Registration of second user
        driver2.get(self.live_server_url)
        signup_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver2.get(signup_navlink)
        sleep(1)
        username_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver2.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver2.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver2.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest2')
        email_textbox.send_keys('systest2@acme.com')
        password1_textbox.send_keys('1337Tests2')
        password2_textbox.send_keys('1337Tests2')
        signup_button.click()
        sleep(1)
        # 1.1 Login
        driver2.get(self.live_server_url)
        signin_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver2.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver2.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest2')
        password_login_textbox.send_keys('1337Tests2')
        login_button.click()
        sleep(1)

        # 2 Joining table
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 2.1 Joining table
        join_game_button = driver2.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 3 Getting proofs
        sleep(2)
        dealer = driver.find_element_by_xpath('//*[@id="dealer"]').text
        self.assertEquals(dealer, 'Dealer: systest')

        # 5 Exit
        exit_game_button = driver.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()
        sleep(2)

        exit_game_button = driver2.find_element_by_xpath('/html/body/div/div/div[1]/button')
        exit_game_button.click()

    def test_120_Check(self):
        driver2 = webdriver.Remote(
            command_executor='http://selenium:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        # signup
        driver = self.selenium
        driver.get(self.live_server_url)
        signup_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver.get(signup_navlink)
        sleep(1)
        username_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver.find_element_by_xpath('/html/body/form/button')
        sleep(1)
        username_textbox.send_keys('systest')
        email_textbox.send_keys('systest@acme.com')
        password1_textbox.send_keys('1337Tests')
        password2_textbox.send_keys('1337Tests')
        signup_button.click()
        sleep(1)
        driver.get(self.live_server_url)
        sleep(1)
        signin_navlink = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest')
        password_login_textbox.send_keys('1337Tests')
        login_button.click()
        sleep(1)
        # 0 Registration of second user
        driver2.get(self.live_server_url)
        signup_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[2]/a').get_attribute('href')
        driver2.get(signup_navlink)
        sleep(1)
        username_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        email_textbox = driver2.find_element_by_xpath('//*[@id="id_email"]')
        password1_textbox = driver2.find_element_by_xpath('//*[@id="id_password1"]')
        password2_textbox = driver2.find_element_by_xpath('//*[@id="id_password2"]')
        signup_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_textbox.send_keys('systest2')
        email_textbox.send_keys('systest2@acme.com')
        password1_textbox.send_keys('1337Tests2')
        password2_textbox.send_keys('1337Tests2')
        signup_button.click()
        sleep(1)
        # 1.1 Login
        driver2.get(self.live_server_url)
        signin_navlink = driver2.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a').get_attribute('href')
        driver2.get(signin_navlink)
        sleep(1)
        username_login_textbox = driver2.find_element_by_xpath('//*[@id="id_username"]')
        password_login_textbox = driver2.find_element_by_xpath('//*[@id="id_password"]')
        login_button = driver2.find_element_by_xpath('/html/body/form/button')

        username_login_textbox.send_keys('systest2')
        password_login_textbox.send_keys('1337Tests2')
        login_button.click()
        sleep(1)

        # 2 Joining table
        join_game_button = driver.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 2.1 Joining table
        join_game_button = driver2.find_element_by_xpath('//*[@id="Test table 1"]/div/a')
        join_game_button.click()

        # 3 Folding
        fold_button = driver.find_element_by_xpath('//*[@id="fold"]')
        sleep(3)
        fold_button.click()

        # 4 Getting proofs
        sleep(1)
        money = driver2.find_element_by_xpath('//*[@id="money-in-table"]').text
        self.assertEquals(money, 'Money: 294')  # Money: 294

    # def test_by_order(self):
    #     SysTests.Index(self)
    #     SysTests.Signup(self)
    #     SysTests.Signin(self)
    #     SysTests.Create_table(self)
    #     SysTests.Join_table(self)
    #     SysTests.Leave_table(self)
    #     SysTests.Chat(self)
    #     SysTests.Game_start(self)
    #     SysTests.Fold(self)
    #     SysTests.Dealer_change(self)
    #     SysTests.Check(self)
