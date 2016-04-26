import socket,datetime,sys
class Http(object):
    """docstring for Http"""
    __sock=()
    __buf=''
    __connection=()
    __address=()
    __option={"host":'localhost',"port":'8991',"listen":5,'timeout':5,'recv_len':8192}
    __responseOption={'status':'200 OK','responseType':'text/html','charset':'utf-8','connection':'keep-alive',}
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
        self.__sock.listen(int(self.__option['listen']));
    def initResponseHeader(self,option):
        self.__responseHeader="HTTP/1.1 "+option['status']+"\nContent-Type: "+option['responseType']+"; charset="+option['charset']+"\nContent-Length: "+option['length']+"\nDate: "+option['date']+"\nConnection: "+option['connection']+"\n\n"
    def __createResponse(self,content,option):
        self.__responseBody=content
        option['length']=str(len(self.__responseBody))
        option['date']=self.__createGMTTime()
        self.initResponseHeader(option);
        print "initResponseHeader Finish"
        return self.__responseHeader+self.__responseBody
    def __createGMTTime(self):
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT';
        return datetime.datetime.utcnow().strftime(GMT_FORMAT);

    def request(self):
        self.__buf=''
        self.__connection,self.__address = self.__sock.accept();
        print self.__connection,self.__address
        try:
            self.__connection.settimeout(int(self.__option['timeout']));
            self.__buf+=self.__recvall(self.__connection)
            # self.__buf = self.__connection.recv(int(self.__option['recv_len']));
            # print self.__buf
        except socket.timeout:
            print 'time out'
    def response(self,option={},content="Hello World"):
        self.__connection.send(self.__createResponse(content,option))
    
    def close(self):
        self.__connection.close()
    def getBuf(self):
        return self.__buf
    def getResponseOption(self):
        return self.__responseOption
    def __recvall(self,sock):
        data = ""
        part = None
        try:
            while part != "":
                sock.setblocking(0)
                part = sock.recv(int(self.__option['recv_len']))
                data += part
        except socket.error, arg:
                (errno, err_msg) = arg
                print "recv failed: %s, errno=%d" % (err_msg, errno)
        print("==============================================================\n")
        return data
