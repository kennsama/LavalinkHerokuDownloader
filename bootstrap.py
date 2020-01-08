"""
Lavalink on Heroku bootstrap script
Credit to diniboy for sed script
"""

from os import system, environ, path, remove
import requests


class LavalinkBootstrap:
	"""
	Class we're using to get Lavalink working on Heroku
	"""

	def __init__(self):

		"""
		Doing important stuff here
		"""

		self.download_command = "wget https://github.com/Frederikam/Lavalink/releases/download/3.2.2/Lavalink.jar"

		self.replace_port_command = 'sed -i "s|DYNAMICPORT|$PORT|" application.yml'

		self.replace_password_command = 'sed -i "s|DYNAMICPASSWORD|$PASSWORD|" application.yml'
		self.replace_password_command_no_password = 'sed -i "s|DYNAMICPASSWORD|youshallnotpass|" application.yml'

		self._additional_options = environ.get(
			"ADDITIONAL_JAVA_OPTIONS"
		)  # Heroku provides basic Java configuration based on dyno size, no need in limiting memory

		self.run_command = "java -jar Lavalink.jar {}".format(self._additional_options)  # User-provided config, will override heroku's

	def replace_password_and_port(self):

		"""
		Replacing password and port in application.yml
		"""

		print(
			"[INFO] Replacing port..."
		)

		try:

			system(
				self.replace_port_command
			)

			if not environ.get("PASSWORD"):
				print(
					"""
					[WARNING] You have not specified your Lavalink password in config vars. To do this, go to settings
					and set the PASSWORD environment variable
					"""
				)

				return system(
					self.replace_password_command_no_password
				)

			system(
				self.replace_password_command
			)

		except BaseException as exc:

			print(
				"[ERROR] Failed to replace port/password. Info: {}.format(exc)"
			)

		else:

			print(
				"[INFO] Done. Config is ready now"
			)

	def download(self):

		"""
		Downloads latest release of Lavalink
		"""

		print(
			"[INFO] Downloading latest release of Lavalink..."
		)

		try:
			if not path.isfile("application.yml"):
				print("[INFO] Downloading application.yml...")
				system("wget -q https://raw.githubusercontent.com/F4stZ4p/HLavalink/master/application.yml")
			system(
				self.download_command
			)

		except BaseException as exc:

			print(
				"[ERROR] Lavalink download failed. Info: {}".format(exc)
			)

		else:

			print(
				"[INFO] Lavalink download OK"
			)

	def run(self):

		"""
		Runs Lavalink instance
		"""

		self.download()
		self.replace_password_and_port()

		print(
			"[INFO] Starting Lavalink..."
		)

		try:

			system(
				self.run_command
			)

		except BaseException as exc:

			print(
				"[ERROR] Failed to start Lavalink. Info: {}".format(exc)
			)


if __name__ == "__main__":

	"""
	Starts our instance
	"""

	LavalinkBootstrap().run()

