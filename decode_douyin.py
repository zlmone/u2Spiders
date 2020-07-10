import json
from handle_mongo import handle_mongodb_save_data


def response(flow):
    # 抖音
    # 个人信息页接口
    # GET https://aweme-eagle-lq.snssdk.com/aweme/v1/user/?user_id...

    # 分享链接item['share_url']
    # www.iesdouyin.com/share/user/813256296637848?sec_uid=...

    # 分享链接json数据
    # https://www.iesdouyin.com/web/api/v2/user/info/?sec_uid=...

    # 滑动视频的接口
    # https://aweme-lq.snssdk.com/aweme/v1/feed...

    # 视频url,每次请求返回7个视频信息
    if 'https://aweme-lq.snssdk.com/aweme/v1/feed' in flow.request.url:
        print('*'*100)
        video_response = json.loads(flow.response.text)
        video_list = video_response.get("aweme_list", [])
        for item in video_list:
            video_item = {}
            # 解析视频链接
            video = item.get("video", "")
            if video:
                play_addr = video.get("play_addr", "")
                if play_addr:
                    url_list = play_addr.get("url_list", "")
                    if url_list:
                        video_item['video_url'] = url_list[0]

            # 其他信息
            author = item.get('author', '')
            if author:
                video_item['unique_id'] = author.get('unique_id', '')
                video_item['short_id'] = author.get('short_id', '')
                video_item['short_id'] = author.get('short_id', '')
                video_item['sec_uid'] = author.get('sec_uid', '')

            video_item['item_type'] = 'douyin_video'
            print(video_item)
            # 保存
            handle_mongodb_save_data(video_item)

            # 发布者页面
    if 'https://aweme-eagle-lq.snssdk.com/aweme/v1/user/?user_id' in flow.request.url:
        print('/' * 100)
        person_response = json.loads(flow.response.text)
        person_info = person_response.get("user", "")
        if person_info:
            info_item = {}
            info_item['nickname'] = person_info.get("nickname", "")
            info_item['unique_id'] = person_info.get("unique_id", 0)
            info_item['short_id'] = person_info.get("short_id", 0)
            share_info = person_info.get("share_info", 0)
            if share_info:
                info_item['share_url'] = share_info.get('share_url', '')

            info_item['country'] = person_info.get("country", "")
            info_item['province'] = person_info.get("province", "")
            info_item['city'] = person_info.get("city", "")

            # 获赞
            info_item['total_favorited'] = person_info.get("total_favorited", 0)
            # 关注
            info_item['following_count'] = person_info.get("following_count", 0)
            # 粉丝
            info_item['follower_count'] = person_info.get("follower_count", 0)

            # 作品
            info_item['aweme_count'] = person_info.get("aweme_count", 0)
            # 喜欢
            info_item['favoriting_count'] = person_info.get("favoriting_count", 0)

            info_item['item_type'] = 'douyin_info'
            print(info_item)
            handle_mongodb_save_data(info_item)
