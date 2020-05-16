# -*- coding: utf-8 -*-
from application import app_fk, db_mysql
import requests, os, time, hashlib, json, re, traceback
from bs4 import BeautifulSoup
from common.lib.DataHelper import getCurrentTime
from urllib.parse import urlparse
from common.model.movie import Movie


# python manager.py runjob -m movie -a list | parse
# 这里不是Command 所以不用继承Command
class Job_task:
    def __init__(self):
        self.source = "btbtdy"
        self.config = {
            "num" : 1,
            "url" : "http://btbtdy1.com/btfl/dy1-#d#.html",     # 这里的#d#是自己添加来下面替换页码的
            "path" : "C:/Users/江林杰/Downloads/tmp/%s/" % self.source
        }

    '''
    第一步 首先 获取列表list html 回来，通过解析html 获取详情 的 url等信息，在根据详情url 获取详情html
    第二步 解析 详情的html
    '''
    def run(self, params):
        act = params['act']
        self.date = getCurrentTime( frm = "%Y%m%d")
        if act == "list":
            self.getList()          # 获取包含电影列表的内容
            self.parseInfo()        # 解析出 电影列表
        elif act == "parse":
            self.parseInfo()        # 根据电影列表解析出 电影详情

    # 获取列表
    def getList(self):
        config = self.config
        path_root = config['path'] + self.date      # 根路径名 = 设置的文件夹路径+日期
        path_list = path_root + "/list"             # list 存放到 根路径下的 list
        path_info = path_root + "/info"             # info 存放到 根路径下的 info
        path_json = path_root + "/json"             # json 存放到 根路径下的 json
        path_vid = path_root + "/vid"               # vid 存放到 根路径下的 vid
        self.makeSuredirs( path_root )              # 确认以上路径均存在（不存在自动创建）
        self.makeSuredirs( path_list )
        self.makeSuredirs( path_info )
        self.makeSuredirs( path_json )
        self.makeSuredirs( path_vid )

        pages = range( 1, config['num'] + 1 )                           # 页面数量 序列
        for idx in pages:                                               # 对每一页进行提取电影信息
            tmp_path = path_list + "/" + str( idx )                     # 存放到 list/页面号  ？
            tmp_url = config['url'].replace("#d#", str( idx ) )         # http://btbtdy1.com/btfl/dy1-#d#.html
            app_fk.logger.info( "get list : " + tmp_url )
            if os.path.exists( tmp_path ):
                continue

            tmp_content = self.getHttpContent( tmp_url )                # 获取content
            self.saveContent( tmp_path, tmp_content )                   # 保存content
            time.sleep(0.3)                                             # 休息

        # os.listdir( path_list ) Return a list containing the names of the files in the directory
        for idx in os.listdir( path_list ):
            tmp_content = self.getContent( path_list + "/" + str( idx ) )
            items_data = self.parseList( tmp_content )                  # 解析出电影列表
            if not items_data:                                          # 空 ==》  退出
                continue

            for item in items_data:                                     # 每个电影item名 用它的hash值
                tmp_json_path = path_json + "/" + item['hash']
                tmp_info_path = path_info + "/" + item['hash']
                tmp_vid_path = path_vid + "/" + item['hash']
                if not os.path.exists( tmp_json_path ):                 # 不存在说明之前没有该电影，下面同理
                    self.saveContent( tmp_json_path, json.dumps( item, ensure_ascii=False ) )

                if not os.path.exists(tmp_info_path):
                    tmp_content = self.getHttpContent( item['info_url'] )    # item['info_url'] 原网站的详情页链接
                    self.saveContent(  tmp_info_path, tmp_content )

                if not os.path.exists( tmp_vid_path ):                  # ？？
                    tmp_content = self.getHttpContent( item['vid_url'] )
                    self.saveContent(  tmp_vid_path, tmp_content )

                time.sleep( 0.3 )

    # 解析出电影列表
    def parseList(self, content):
        data = []
        config = self.config
        url_info = urlparse( config['url'] )                    # 链接解析器return： 链接类型， 链接
        url_domain = url_info[0] + "://" + url_info[1]          # 原网页的链接不完整，补充完整；这里是前半部分
        # 进行解析
        tmp_soup = BeautifulSoup( str(content), "html.parser" )
        tmp_list = tmp_soup.select( "div.list_su ul li" )
        for tmp_item in tmp_list:
            tmp_target = tmp_item.select("a.pic_link")
            tmp_name = tmp_target[0]['title']
            tmp_href = tmp_target[0]['href']
            if "http:" not in tmp_href:                         # 补充成完整链接
                tmp_href = url_domain + tmp_href
            tmp_vid_url = tmp_href.replace("btdy/dy", "vidlist/")
            tmp_data = {
                "name" : tmp_name,
                "info_url" : tmp_href,
                "vid_url" : tmp_vid_url,
                "hash" :  hashlib.md5( tmp_href.encode("utf-8") ).hexdigest()
            }
            data.append( tmp_data )

        return data

    # 解析出详情信息
    def parseInfo(self):
        print(" in the parseInfo ")
        config = self.config
        path_root = config['path'] + self.date
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        path_vid = path_root + "/vid"
        for filename in os.listdir(  path_info ):
            tmp_json_path = path_json + "/" + filename
            tmp_info_path = path_info + "/" + filename
            tmp_vid_path = path_vid + "/" + filename

            tmp_data = json.loads( self.getContent( tmp_json_path), encoding="utf-8")
            tmp_content = self.getContent( tmp_info_path )
            tmp_soup = BeautifulSoup( tmp_content, "html.parser")   # 解析详情页 content
            try:
                tmp_pub_date = tmp_soup.select( "div.vod div.vod_intro dl dd" )[0].getText()
                tmp_desc = tmp_soup.select( "div.vod div.vod_intro div.des" )[0].getText()
                tmp_classify = tmp_soup.select( "div.vod div.vod_intro dl dd" )[2].getText()
                tmp_actor = tmp_soup.select( "div.vod div.vod_intro dl dd" )[6].getText()
                tmp_pic_list = tmp_soup.select("div.vod div.vod_img img")
                tmp_pics = []
                for tmp_pic in tmp_pic_list:
                    tmp_pics.append( tmp_pic['src'] )

                # 获取下载地址
                tmp_download_content = self.getContent( tmp_vid_path  )
                tmp_vid_soup = BeautifulSoup( tmp_download_content ,"html.parser")
                tmp_download_list = tmp_vid_soup.findAll( "a",href = re.compile( "magnet:?" ) )
                tmp_magnet_url = ""
                if tmp_download_list:
                    tmp_magnet_url = tmp_download_list[0]['href']

                tmp_data['pub_date'] = tmp_pub_date
                tmp_data['description'] = tmp_desc
                tmp_data['classification'] = tmp_classify
                tmp_data['actors'] = tmp_actor
                tmp_data['magnet_url'] = tmp_magnet_url
                tmp_data['source'] = self.source
                tmp_data['create_time'] = tmp_data['update_time'] = getCurrentTime()
                if tmp_pics:
                    tmp_data['cover_pic'] = tmp_pics[0]
                    tmp_data['pics'] = json.dumps( tmp_pics )
                # print("tmp-data to mysql db: 1111111111")

                tmp_movie_info = Movie.query.filter_by(hash = tmp_data['hash']).first()

                if tmp_movie_info:
                    continue
                # 写入数据库
                print("tmp-data to mysql db:2222222222222222")
                print(tmp_data)
                tmp_model_movie = Movie(**tmp_data)
                db_mysql.session.add(tmp_model_movie)
                db_mysql.session.commit()

            except:
                continue
        return True

    # 获取 content
    def getHttpContent(self, url):
        try:
            headers = {
              'Content-Type': 'text/html;charset=utf-8',
              'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
              'Referer' : "http://btbtdy1.com/btdy/dy18196.html",
              "Accept" : "text/html,application/xhtml+xml,application/xml;"
                         "q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
            }
            r = requests.get( url , headers=headers)
            if r.status_code != 200 :
                return None

            return r.content

        except Exception:
            return None

        '''
        try:
            print(url)
            r = requests.get( url )
            if r.status_code != 200 :
                return None
            return r.content

        except Exception:
            return None

        '''



    # 把content文件写到本地
    def saveContent(self, path, content):
        if content:
            with open( path, mode="w+", encoding="utf-8" ) as f:
                if type(content) != str:
                    content = content.decode("utf-8")

                f.write(content )
                f.flush()
                f.close()

    # 从本地读取 content 文件
    def getContent(self, path):
        if os.path.exists( path ):
            with open( path, "r", encoding="utf-8 ") as f:
                return f.read()

        return ''

    # 确认 路径存在
    def makeSuredirs(self,path):
        if not os.path.exists( path ):
            os.makedirs( path )
