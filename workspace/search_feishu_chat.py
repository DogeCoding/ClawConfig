
import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *

def main():
    # 创建client
    client = lark.Client.builder() \
        .app_id("cli_a934dc3183389cb6") \
        .app_secret("nRKMmPSH7QvqlyZlSmyl5guce5NQPBiZ") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    # 构造请求对象
    request: SearchChatRequest = SearchChatRequest.builder() \
        .user_id_type("open_id") \
        .query("News") \
        .page_size(20) \
        .build()

    # 发起请求
    response: SearchChatResponse = client.im.v1.chat.search(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.chat.search failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: {json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    print("搜索结果：")
    print(lark.JSON.marshal(response.data, indent=4))

if __name__ == "__main__":
    main()

