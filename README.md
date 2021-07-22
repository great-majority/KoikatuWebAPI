# KoikatuWebAPI
Web API wrapper for Koikatu / EmotionCreators official uploader.

# Basic Usage

```python
>>> from kkwebapi import KoikatuWebAPI
>>> df = KoikatuWebAPI.get_ranking()
>>> print(df)
          id  sex  height  bust  hair  personality  blood_type  ...    name  nickname handle_name            comment download_num                                                uid  weekly_download_num
0          1    1       1     2     2            0           3  ...   高岡 結香        ユイ    ILLUSION       ILLUSIONサンプル         1256  gOuAD02g92pX05r3Sj2aJJeJ01FdWqh01pe5PM1284vK01...                    6
...
```