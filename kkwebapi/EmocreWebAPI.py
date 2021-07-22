import base64
import io
import zipfile

import pandas as pd
import requests


class EmocreWebAPI:
    uploader_url = "http://upemocre.illusion.jp/manipulate_user_table_from_game.php"
    map_list_url = "http://upemocre.illusion.jp/manipulate_uploader_from_game_map.php"
    pose_list_url = "http://upemocre.illusion.jp/manipulate_uploader_from_game_pose.php"
    scene_list_url = (
        "http://upemocre.illusion.jp/manipulate_uploader_from_game_scene.php"
    )
    chara_list_url = (
        "http://upemocre.illusion.jp/manipulate_uploader_from_game_chara.php"
    )

    headers = {
        "User-Agent": "UnityPlayer/2017.4.24f1 (UnityWebRequest/1.0, libcurl/7.51.0-DEV)",
        "X-Unity-Version": "2017.4.24f1",
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

    @classmethod
    def user_list(cls):
        datas = {
            "mode": 3,
        }
        data_types = [
            ("user_id", "int"),  # 作者ID
            ("user_name", "str"),  # 作者名
            ("map_score", "int"),  # 全マップの総評価点
            ("pose_score", "int"),  # 全ポーズの総評価点
            ("scene_score", "int"),  # 全シーンの総評価点
            ("map_evaluation", "int"),  # マップを評価された回数
            ("pose_evaluation", "int"),  # ポーズを評価された回数
            ("scene_evaluation", "int"),  # シーンを評価された回数
        ]
        return cls._from_tab_table(cls.uploader_url, datas, data_types)

    @classmethod
    def chara_list(cls):
        datas = {"mode": 0}
        data_types = [
            ("id", "int"),  # 作品ID
            ("guid", "str"),  # GUID
            ("user_id", "int"),  # 作者ID
            ("name", "str"),  # キャラクター名
            ("voice_type", "int"),  # キャラクターの音声タイプ 男は99
            ("birth_month", "int"),  # 誕生月
            ("birth_day", "int"),  # 誕生日
            ("blood_type", "int"),  # 血液型
            ("comment", "str"),  # コメント
            ("chara_packs", "str"),  # キャラ使用パック
            ("sex", "int"),  # 10 性別 0:男 1:女
            ("height", "int"),  # 11 身長
            ("bust", "int"),  # 12 胸囲 男は99
            ("hair", "int"),  # 13 髪型
            ("download", "int"),  # 総ダウンロード数
            ("weekly_download", "int"),  # 週間ダウンロード数
            ("update_time", "str"),  # 最終更新日時
            ("num_update", "int"),  # 更新回数
            ("upload_time", "str"),  # アップロード日時
        ]
        return cls._from_tab_table(cls.chara_list_url, datas, data_types)

    @classmethod
    def map_list(cls):
        datas = {"mode": 0}
        data_types = [
            ("id", "int"),  # 作品ID
            ("guid", "str"),  # GUID
            ("user_id", "int"),  # 作者ID
            ("title", "str"),  # マップ名
            ("uses_mapset", "bool"),  # マップセットの使用
            ("object_num", "int"),  # 使用オブジェクト数
            ("comment", "str"),  # コメント
            ("map_packs", "str"),  # マップ使用パック
            ("download", "int"),  # 総ダウンロード数
            ("weekly_download", "int"),  # 週間ダウンロード数
            ("update_time", "str"),  # 最終更新日時
            ("num_update", "int"),  # 更新回数
            ("score", "int"),  # 総評価得点
            ("num_evaluation", "int"),  # 総評価回数
            ("upload_time", "str"),  # アップロード日時
        ]
        return cls._from_tab_table(cls.map_list_url, datas, data_types)

    @classmethod
    def pose_list(cls):
        datas = {"mode": 0}
        data_types = [
            ("id", "int"),  # 作品ID
            ("guid", "str"),  # GUID
            ("user_id", "int"),  # 作者ID
            ("title", "str"),  # ポーズ名
            ("comment", "str"),  # コメント
            ("download", "int"),  # 総ダウンロード数
            ("weekly_download", "int"),  # 週間ダウンロード数
            ("update_time", "str"),  # 最終更新日時
            ("num_update", "int"),  # 更新回数
            ("score", "int"),  # 総評価得点
            ("num_evaluation", "int"),  # 総評価回数
            ("upload_time", "str"),  # アップロード日時
        ]
        return cls._from_tab_table(cls.pose_list_url, datas, data_types)

    @classmethod
    def scene_list(cls):
        datas = {"mode": 0}
        data_types = [
            ("id", "int"),  # 作品ID
            ("guid", "str"),  # GUID
            ("user_id", "int"),  # 作者ID
            ("title", "str"),  # 作品名
            ("uses_mapset", "bool"),  # マップセットの使用
            ("object_num", "int"),  # 使用オブジェクト数
            ("num_male", "int"),  # 男キャラ数
            ("num_female", "int"),  # 女キャラ数
            ("contains_adv", "bool"),  # ADVパートを含むか
            ("contains_h", "bool"),  # Hパートを含むか
            ("tags", "str"),  # タグ
            ("comment", "str"),  # コメント
            ("map_packs", "str"),  # マップ使用パック
            ("chara_packs", "str"),  # キャラ使用パック
            ("download", "int"),  # 総ダウンロード数
            ("weekly_download", "int"),  # 週間ダウンロード数
            ("update_time", "str"),  # 最終更新日時
            ("num_update", "int"),  # 更新回数
            ("score", "int"),  # 総評価得点
            ("num_evaluation", "int"),  # 総評価回数
            ("num_played", "int"),  # 総プレイ回数
            ("upload_time", "str"),  # アップロード日時
        ]
        return cls._from_tab_table(cls.scene_list_url, datas, data_types)

    @classmethod
    def get_scene(cls, index, count=False):
        datas = {"mode": 4, "index": index, "add_count": 1 if count else 0}
        res = requests.post(cls.scene_list_url, datas, headers=cls.headers)
        splitted = res.text.split("\t")
        image_zip = base64.b64decode(splitted[1])
        if int(splitted[0]) == 1:
            with zipfile.ZipFile(io.BytesIO(image_zip)) as zip_bin:
                image = zip_bin.read(zip_bin.infolist()[0])
        else:
            image = image_zip
        return image
