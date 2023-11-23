import time
from datetime import datetime

summary_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
           "Phasellus feugiat dapibus sagittis. Sed sit amet eleifend odio. " \
           "In justo tellus, porttitor ac eleifend a, viverra ac dolor." \
           " Phasellus bibendum pretium ipsum, id congue leo consequat eget. " \
           "In hac habitasse platea dictumst. Etiam blandit metus in tincidunt rutrum. " \
           "Nunc lacinia urna quis est commodo rutrum. Integer sed dui id felis tempor pretium. " \
           "Donec accumsan id velit quis cursus. Ut a accumsan lacus. Pellentesque porta scelerisque tellus," \
           " a vehicula felis pellentesque in. " \
           "Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; " \
           "Vivamus non dui vitae lacus euismod rhoncus non eu justo. Sed tortor mi, ullamcorper ac faucibus sit amet," \
           " rutrum vitae augue."

record = {"title": "Example Video",
              "duration": "120",
              "source": "local",
              "publication_date": "2022-12-03" }
record2 = {"title": "sad asdf 2",
              "duration": "120",
              "source": "local",
              "publication_date": "2022-12-03" }

summary_score = 80
summary_state = "positive"
timestamp_generated = datetime.now()

result = {
    "summary_score": 80,
    "summary_text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus feugiat dapibus sagittis. Sed sit amet eleifend odio. In justo tellus, porttitor ac eleifend a, viverra ac dolor. Phasellus bibendum pretium ipsum, id congue leo consequat eget. In hac habitasse platea dictumst. Etiam blandit metus in tincidunt rutrum. Nunc lacinia urna quis est commodo rutrum. Integer sed dui id felis tempor pretium. Donec accumsan id velit quis cursus. Ut a accumsan lacus. Pellentesque porta scelerisque tellus, a vehicula felis pellentesque in. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vivamus non dui vitae lacus euismod rhoncus non eu justo. Sed tortor mi, ullamcorper ac faucibus sit amet, rutrum vitae augue.",
    "timestamp_generated": "Sat, 04 Nov 2023 19:36:54 GMT",
    "video_id": "65468f4a945184328eb2cd62"
}