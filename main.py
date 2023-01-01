import urllib.request
import json
import subprocess

path = __file__.split("/") 
path.pop()
path = "/".join(path)

def is_new_version(version_tag):
	file_path = f"{path}/version.txt"
	
	# create file if don't exist
	f = open(file_path, "a+")
	f.close()

	with open(file_path, "r") as f:
		saved_version = f.read()

	if version_tag == saved_version:
		print("No new version")
		return False
	else:
		with open(file_path, "w") as f:
			f.write(version_tag)
		return True

def build(version_tag):
	command = f"docker build --tag localbuild/caddy-cloudflare:latest --tag deriando/caddy-cloudflare:latest --tag deriando/caddy-cloudflare:{version_tag} {path}"
	arr = command.split()
	process = subprocess.run(arr)
	return process.returncode

def push():
	command = f"docker image push --all-tags deriando/caddy-cloudflare"
	arr = command.split()
	process = subprocess.run(arr)
	return process.returncode

def main():
	with urllib.request.urlopen("https://api.github.com/repos/caddyserver/caddy/tags") as response:
		r = response.read()
		r = json.loads(r)
		version_tag = r[0]['name']
		if is_new_version(version_tag):
			build(version_tag)
			push()
			return 0


if __name__ == "__main__":
	main()