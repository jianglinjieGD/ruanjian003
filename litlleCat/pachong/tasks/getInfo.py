# 文件名： getMovies.py
from flask_script import Command
import requests
from bs4 import BeautifulSoup as bs     # 解析网页内容
from common.model.movie import Movie
from application import db_mysql
import datetime

# !!! 规范化： 所有的job模块都使用 Job_task 作为类名
# 使用模块文件的名字来区分
# 需要继承Command，才会默认执行run函数
class Job_task(Command):
    def run(self, params):
        s = {
            'name': 'Re：从零开始的异世界生活 冰结之绊',
            'info_url': 'http://btbtdy1.com/btdy/dy23876.html',
            'vid_url': 'http://btbtdy1.com/vidlist/23876.html'
,           'hash': 'fb5674fbac0285a01f4638576053fee2',
            'pub_date': '2020-05-07 16:36',
            'description': '剧情介绍：如果是为了你的话，我可以成为任何东西——。'
                           '继2018年秋剧场上映的《Re:从零开始的异世界生活 Memory Snow》之后， 动画完全新作篇章第2弹。'
                           ' 女主角爱蜜莉雅与精灵帕克相遇，被召唤至罗兹瓦尔宅邸之前的故事。 描写一直生活在艾利欧鲁大森林的'
                           '爱蜜莉雅面临露格尼卡王国王选之前的故事，TV系列的前日谭。',
            'classification': '电影 / 奇幻\xa0/\xa0动画\xa0/\xa0冒险',
            'actors': '高桥李依\xa0/\xa0内山夕实\xa0/\xa0小林裕介\xa0/\xa0水濑祈\xa0/\xa0村川梨衣\xa0/\xa0子安武人',
            'magnet_url': 'magnet:?xt=urn:btih:63cb6c3085228060a737946bb7da7bea78c822f2',
            'source': 'btbtdy',
            'create_time': '2020-05-08 15:21:03',
            'update_time': '2020-05-08 15:21:03',
            'cover_pic': 'http://gif-china.cc/uploads/allimg/202004/817282df9c4ba90b.jpg?h=250',
            'pics': '["http://gif-china.cc/uploads/allimg/202004/817282df9c4ba90b.jpg?h=250"]'
        }

        # mo = Movie(movie_id=1, description="default description", pub_date="2020/02/02")
        mo = Movie(**s)
        db_mysql.session.add(mo)
        db_mysql.session.commit()
        return

