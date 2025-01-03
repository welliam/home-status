import os
import tempfile
import neocities
from datetime import datetime


API_KEY = os.environ.get("NEOCITIES_API_KEY")

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def open_log(mode="r"):
    return open(os.path.join(__location__, "log.txt"), mode=mode)


def upload_strings(files: dict[str, bytes | str]):
    """
    files is a dict {filename: content}
    """

    CHUNK_SIZE = 25

    def _temp_file_of(content: str | bytes):
        if type(content) == str:
            review_file = tempfile.NamedTemporaryFile(mode="w")
        else:
            review_file = tempfile.NamedTemporaryFile(mode="wb")

        review_file.write(content)
        review_file.seek(0)
        return review_file

    file_objects = {
        neocities_path: _temp_file_of(content)
        for neocities_path, content in files.items()
    }
    file_list = [
        (file.name, neocities_path) for neocities_path, file in file_objects.items()
    ]

    if API_KEY:
        client = neocities.NeoCities(api_key=API_KEY)
        client.upload(*file_list)
    else:
        print(file_list)
    # for index, chunk in enumerate(chunkify(list(file_list), CHUNK_SIZE)):
    #     logging.info(f"Uploading chunk of size {len(chunk)}")
    #     client.upload(*chunk)
    #     if index != 0:
    #         sleep(3)


now = datetime.now()

lines = open_log().read()

with open_log("w") as f:
    f.write(str(now))
    f.write("\n")
    f.writelines(lines)


lines = "\n".join([f"<li>{line}</li>" for line in open_log().read().strip().split("\n")[:100]])

script = """
    <script>
      const latest = new Date(Array.from(document.querySelectorAll(".list li"))[0].innerHTML)
      const minutes = (new Date() - latest) / 1000 / 60
      document.body.innerHTML = `<span>I am <b>${minutes < 10.1 ? "online" : "offline"}</b>!</span>` + document.body.innerHTML
    </script>
"""

html = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Home status</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <body>
    <ul class="list">{lines}</ul>
    {script}
  </body>
</html>
"""

if API_KEY:
    upload_strings({"home-status.html": html})
else:
    print(html)
