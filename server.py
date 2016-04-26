import os
import mimetypes
import sys
import copy

from http import Http
from tools import Tools

class Server:
    __http=()
    __requestHeader={}
    __tools=()
    def __init__(self,option={}):
        self.__http=Http(option)
        self.__tools=Tools()

    def run(self):

        while True:
            self.__http.request()
            self.dealRequest()
            res=self.dealResponse()
            self.__http.response(option=res['option'],content=res['content'])
            self.__http.close()

    def dealRequest(self):
        self.__requestHeader={}
        buf=self.__http.getBuf().splitlines()
        new_buf = [b.split(':',1) for b in buf]
        # print buf
        if len(new_buf)<=0:
            self.__requestHeader['resources']='404'
            return False

        header=new_buf[0][0].split(' ')
        new_buf.pop(0)

        self.__requestHeader['method']=header[0]
        self.__requestHeader['resources']=header[1].split('?')[0]
        if '?' in header[1]:
            self.__requestHeader['param']=header[1].split('?')[1]

        self.__requestHeader['protocol']=header[2]
        for b in new_buf:
            if  b[0].strip(' ') != '':
                self.__requestHeader[b[0].strip(' ').replace('-','_').lower()]=b[1].strip(' ')
        # print self.__requestHeader
        return new_buf

    def dealResponse(self):
        root='E:/users/huajie/documents/python/http/lightSnake/htdocs'
        defaultFile='index.html'
        path=root+self.__requestHeader['resources']
        if self.__requestHeader['resources'].strip('/')=='':
            path=path.strip('/')+'/'+defaultFile
        # print path
        defaultOption= copy.deepcopy(self.__http.getResponseOption())
        data={'option':defaultOption,'content':' '}
        print data
        # <h1>Hello World</h1>
        # (fileExtension,name)=mimetypes.guess_extension(path)
        (responseType,name)=mimetypes.guess_type(path)
        print os.path.exists(path)
        if os.path.exists(path):
            if 'text/' in responseType:
                file = open(path)
            else:
                file = open(path,'rb')
            try:
                fileText = file.read()
                data['content']= fileText
                data['option']['responseType']=responseType
                data['charset']=''
                # file.close()
            except IOError:
                print IOError.message
            finally:
                file.close()
            print "if"
        else:
            print "else"
            data['option']['status']='404 Not Found'

        return data

    def getFileType(self,fileName):
        return os.path.splitext(fileName)


if __name__ == '__main__':
    print "start"
    s=Server()
    s.run()