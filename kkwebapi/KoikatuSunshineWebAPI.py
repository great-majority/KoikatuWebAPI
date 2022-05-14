import base64
import io

import pandas as pd
import requests


class KoikatuSunshineWebAPI:
    charas_url = "http://upks.illusion.jp/api/chara.php"
    users_url = "http://upks.illusion.jp/api/user.php"
    headers = {
        "User-Agent": "UnityPlayer/2019.4.9f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)",
        "X-Unity-Version": "2019.4.9f1",
    }

    @classmethod
    def _from_tab_table(cls, url, params, data_types):
        res = requests.post(url, params, cls.headers)
        columns = list(map(lambda x: x[0], data_types))
        df = pd.read_csv(io.StringIO(res.text), sep="\t", header=None, names=columns)
        df = df.applymap(
            lambda x: base64.b64decode(x).decode("utf-8") if not pd.isnull(x) else ""
        )
        df = df.astype(dict(data_types))
        return df

    @staticmethod
    def decode_chara(line):
        c = line.split("\t")
        return list(map(lambda x: base64.b64decode(x).decode("utf-8"), c))

    @classmethod
    def get_charas(cls):
        datas = {"mode": 0}
        data_types = [
            ("id", "int"),  # 作品ID
            ("guid", "str"),  # GUID
            ("user_id", "int"),  # 作者ID
            ("name", "str"),  # キャラ名
            ("nickname", "str"),  # ニックネーム
            ("personality", "int"),  # 性格
            ("birthmonth", "int"),  # 誕生月
            ("birthday", "int"),  # 誕生日
            ("blood_type", "int"),  # 血液型
            ("purpose", "int"),  # 滞在目的
            ("comment", "str"),  # コメント
            ("sex", "int"),  # 性別
            ("height", "int"),  # 身長
            ("bust", "int"),  # 胸囲
            ("hair", "int"),  # 髪型
            ("download_1", "int"),  #
            ("download_2", "int"),  #
            ("good", "int"),  # "拍手"の回数
            ("update_time", "str"),  # 更新日時
            ("update_count", "int"),  # 更新回数
            ("upload_time", "str"),  # アップロード日時
        ]
        return cls._from_tab_table(cls.charas_url, datas, data_types)

    @classmethod
    def get_users(cls):
        datas = {"mode": 2}
        data_types = [
            ("id", "int"),  # 作品ID
            ("name", "str"),  # GUID
        ]
        return cls._from_tab_table(cls.users_url, datas, data_types)

    @classmethod
    def fetch_chara(cls, index, add_count=0):
        datas = {"mode": 4, "index": index, "add_count": add_count}
        response = requests.post(cls.charas_url, datas, cls.headers).text.split("\t")
        return base64.b64decode(response[1])
