import socket,datetime,sys
class Http(object):
    """docstring for Http"""
    __sock=()
    __buf=''
    __connection=()
    __address=()
    __option={"host":'localhost',"port":'8991',"listen":5,"responseType":'text/html',"charset":'utf-8','connection':'keep-alive','timeout':5,'recv_len':4096}
    __content=''
    __responseHeader=''
    __responseBody=''
    def __init__(self, option={}):
        self.initSocket(option);
        print "initSocket Finish"
        
        
    def initSocket(self,option):
        for k,v in option.items():
            if self.__option.has_key(k):
                self.__option[k]=v
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
        self.__sock.bind((self.__option['host'], int(self.__option['port'])));
        self.__sock.listen(self.__option['listen']);
    def initResponseHeader(self):
        date=self.__createGMTTime();
        self.__responseHeader="HTTP/1.1 200 OK\nContent-Type: "+self.__option['responseType']+"; charset="+self.__option['charset']+"\nContent-Length: "+str(len(self.__responseBody))+"\nDate: "+date+"\nConnection: "+self.__option['connection']+"\n\n"
    def __createResponse(self):
        self.initResponseHeader();
        print "initResponseHeader Finish"
        return self.__responseHeader+self.__responseBody
    def __createGMTTime(self):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT';
        return datetime.datetime.utcnow().strftime(GMT_FORMAT);

    def start(self,content):       
        self.__responseBody=content
        while True:
            self.__connection,self.__address = self.__sock.accept();
            print self.__connection,self.__address
            try:
                self.__connection.settimeout(self.__option['timeout']);
                self.__buf = self.__connection.recv(self.__option['recv_len']);
                self.__connection.send(self.__createResponse())
                print self.__buf
            except socket.timeout:
                print 'time out'
            self.__connection.close()


if __name__ == '__main__':
    http=Http();
    http.start(content="It's OverWorks")