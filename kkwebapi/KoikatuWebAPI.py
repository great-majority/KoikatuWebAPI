import base64

import pandas as pd
import requests


class KoikatuWebAPI:
    # {"mode":1, "trial":1} 全取得 0でも同じ?
    # {"mode":2, "pid":"99999\n99998"} 指定したやつのサムネイルをダウンロード
    # {"mode":3, ...} 画像のアップロード
    # {"mode":4, "pid":99999} 指定したやつの本体をダウンロード(カウンターの値が上昇する)
    # {"mode":5, "pid":99999, "uid","sasasa"} 画像の削除

    ranking_url = (
        "http://up.illusion.jp/koikatu_upload/chara/master/unity/koikatu_getChara.php"
    )
    web_image_url = "http://up.illusion.jp/koikatu_upload/chara/download.php/security/koikatu{}/products_id/{}/cPath/0"
    headers = {
        "User-Agent": "UnityPlayer/5.6.2f1 (http://unity3d.com)",
        "X-Unity-Version": "5.6.2f1",
    }
    columns = [
        "id",
        "sex",
        "height",
        "bust",
        "hair",
        "personality",
        "blood_type",
        "day_of_birth",
        "club",
        "name",
        "nickname",
        "handle_name",
        "comment",
        "download_num",
        "uid",
        "weekly_download_num",
    ]

    @classmethod
    def get_ranking(cls):
        body = {"mode": 1, "trial": 0}
        res = requests.post(cls.ranking_url, body, headers=cls.headers).text
        datas = list(map(lambda x: cls.decode_chara(x), res.split("\n")))
        return pd.DataFrame(datas, columns=cls.columns)

    @classmethod
    def get_image(cls, image_id):
        body = {"mode": 4, "pid": image_id}
        res = requests.post(cls.ranking_url, body, headers=cls.headers).content
        res = base64.b64decode(res)
        return res

    @classmethod
    def get_image_from_web(cls, image_id):
        url = cls.web_image_url.format(str(image_id).zfill(7), image_id)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0",
            "Referer": "http://up.illusion.jp/koikatu_upload/chara/",
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        image = res.content
        return image

    @staticmethod
    def decode_chara(line):
        c = line.split("\t")
        chara = [
            int(c[0]),
            int(c[1]),
            int(c[2]),
            int(c[3]),
            int(c[4]),
            int(c[5]),
            int(c[6]),
            base64.b64decode(c[7]).decode("utf-8"),
            int(c[8]),
            base64.b64decode(c[9]).decode("utf-8"),
            base64.b64decode(c[10]).decode("utf-8"),
            base64.b64decode(c[11]).decode("utf-8"),
            base64.b64decode(c[12]).decode("utf-8"),
            int(c[14]),
            c[13],
            int(c[15]),
        ]
        return chara


def save_to_csv(filename):
    r = KoikatuWebAPI.get_ranking()
    r.to_csv(filename, index=None)


def save_image(filename, id, webaccess=False):
    if webaccess:
        image = KoikatuWebAPI.get_image_from_web(id)
    else:
        image = KoikatuWebAPI.get_image(id)
    with open(filename, "wb+") as f:
        f.write(image)


# 指定した投稿者の概要を表示
def print_stat_poster(handle_name):
    r = KoikatuWebAPI.get_ranking()
    # 正しいランキング
    r["rank"] = r["download_num"].rank(ascending=False, method="min").astype("int32")
    poster = r[r["handle_name"] == handle_name].copy()
    # 同率ダウンロード数のキャラ数
    poster["tie"] = poster["download_num"].map(lambda x: (r["download_num"] == x).sum())
    # 全体の上位何％か
    poster["above"] = 1 - (poster["rank"] - 1) / len(r)
    print_columns = [
        "id",
        "name",
        "download_num",
        "weekly_download_num",
        "rank",
        "tie",
        "above",
    ]
    print(poster[print_columns])


# 1, 10, 50, 100, 500, 1000, 5000, 10000位のダウンロード数を表示
def print_download_num(rank=[0, 9, 49, 99, 499, 999, 4999, 9999]):
    r = KoikatuWebAPI.get_ranking()
    r["rank"] = r["download_num"].rank(ascending=False, method="min").astype("int32")
    r["above"] = 1 - r["rank"] / len(r)
    r_s = r.sort_values("download_num", ascending=False)[
        ["rank", "id", "download_num", "weekly_download_num", "above"]
    ].iloc[rank]
    print(r_s)
