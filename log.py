import os
import tempfile
import neocities
from datetime import datetime


API_KEY = os.environ["NEOCITIES_API_KEY"]


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

    client = neocities.NeoCities(api_key=API_KEY)
    looped = False
    client.upload(*file_list)
    # for index, chunk in enumerate(chunkify(list(file_list), CHUNK_SIZE)):
    #     logging.info(f"Uploading chunk of size {len(chunk)}")
    #     client.upload(*chunk)
    #     if index != 0:
    #         sleep(3)


now = datetime.now()

lines = open("log.txt").read()

with open("log.txt", "w") as f:
    f.write(str(now))
    f.write("\n")
    f.writelines(lines)


lines = "\n".join([f"<li>{line}</li>" for line in open("log.txt").read().strip().split("\n")])

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
  <body>
    <ul class="list">{lines}</ul>
    {script}
  </body>
</html>
"""

upload_strings({"home-status.html": html})
